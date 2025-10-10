#!/usr/bin/env python3
# One-Time-Pad + Wegman–Carter MAC (polynomial hash mod 2^127-1), single-file CLI.
# SECURITY MODEL:
#  - Vertraulichkeit: OTP (C = M XOR Kenc), Kenc einmalig!
#  - Integrität: Tag = H_r(M) XOR K2, mit pro-Nachricht frischem r und K2 (beides aus dem Pad).
#    Fälschungs-Chance ≈ 2^-128 (informationstheoretisch), wenn r und K2 je Nachricht frisch sind.
#  - PAD BYTES DÜRFEN NIE WIEDERVERWENDET WERDEN. Offset-Management ist kritisch.

import argparse, json, os, sys, hashlib, binascii
from pathlib import Path
from typing import Tuple

PAD_STATE_VERSION = 1
TAG_LEN = 16  # 128-bit Tag
R_LEN   = 16  # 128-bit r für Poly-Hash
P = (1 << 127) - 1  # Mersenne-Prime 2^127 - 1

# ---------- Hilfsfunktionen ----------
def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def load_pad_info(pad_path: Path) -> dict:
    if not pad_path.exists():
        raise SystemExit(f"[ERR] Pad-Datei fehlt: {pad_path}")
    size = pad_path.stat().st_size
    with pad_path.open("rb") as f:
        prefix = f.read(64)
    return {
        "pad_id": sha256(prefix + size.to_bytes(16, "big")),
        "size": size,
    }

def state_path_for(pad_path: Path) -> Path:
    return pad_path.with_suffix(pad_path.suffix + ".state.json")

def load_or_init_state(pad_path: Path) -> dict:
    st_path = state_path_for(pad_path)
    if st_path.exists():
        st = json.loads(st_path.read_text(encoding="utf-8"))
        # sanity
        if st.get("version") != PAD_STATE_VERSION:
            raise SystemExit("[ERR] Pad-State-Version passt nicht.")
        return st
    # neu
    info = load_pad_info(pad_path)
    st = {
        "version": PAD_STATE_VERSION,
        "pad_file": str(pad_path),
        "pad_id": info["pad_id"],
        "offset": 0,
        "consumed": 0,
        "size": info["size"],
    }
    st_path.write_text(json.dumps(st, indent=2), encoding="utf-8")
    return st

def save_state(pad_path: Path, st: dict) -> None:
    st_path = state_path_for(pad_path)
    tmp = st_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, indent=2), encoding="utf-8")
    tmp.replace(st_path)

def reserve_pad(pad_path: Path, nbytes: int) -> int:
    """Reserviert nbytes im Pad ab aktuellem offset, atomar via State-Datei (Single-Process)."""
    st = load_or_init_state(pad_path)
    off = st["offset"]
    if off + nbytes > st["size"]:
        raise SystemExit("[ERR] Pad erschöpft (zu wenig Bytes).")
    st["offset"] = off + nbytes
    st["consumed"] += nbytes
    save_state(pad_path, st)
    return off

def read_pad_slice(pad_path: Path, off: int, n: int) -> bytes:
    with pad_path.open("rb") as f:
        f.seek(off)
        return f.read(n)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def chunks(b: bytes, w: int) -> list:
    return [b[i:i+w] for i in range(0, len(b), w)]

def int_from_le(b: bytes) -> int:
    return int.from_bytes(b, "little")

def int_to_le(x: int, n: int) -> bytes:
    return int(x).to_bytes(n, "little")

# ---------- Polynomial Hash mod 2^127-1 ----------
def reduce_m127(x: int) -> int:
    # Reduktion mod (2^127-1): x mod p = (x & (p)) + (x >> 127); ggf. ein- bis zweimal nachjustieren
    x = (x & P) + (x >> 127)
    if x >= P:
        x -= P
    return x

def poly_hash_mod_p(msg: bytes, r_bytes: bytes) -> int:
    """
    H_r(M) = sum_{i=0..k-1} m_i * r^i (mod p),
    mit 16-Byte Blöcken m_i (little-endian), r in [1, p-1]
    -> Ergebnis als 128-bit Wert (wir geben 16 Byte aus, reduziert mod p).
    """
    # r ∈ [1, p-1]
    r = int_from_le(r_bytes) % P
    if r == 0:
        r = 1
    acc = 0
    # in 16-Byte-Blöcken hashen (letzten Block mit Nullen auffüllen)
    for i, blk in enumerate(chunks(msg + b"\x00"*((16 - len(msg)%16) % 16), 16)):
        mi = int_from_le(blk)
        if i == 0:
            acc = mi % P
        else:
            acc = reduce_m127((acc * r) % P)
            acc = reduce_m127((acc + mi) % P)
    return acc  # < p

# ---------- Envelope ----------
def build_header(version: int, pad_id: str, off_enc: int, off_r: int, off_k2: int, msg_len: int) -> dict:
    return {
        "enc": "OTP+WC",
        "version": version,
        "pad_id": pad_id,
        "offset_enc": off_enc,
        "offset_r": off_r,
        "offset_k2": off_k2,
        "len": msg_len,
        "tag_len": TAG_LEN,
        "r_len": R_LEN,
        "p": "2^127-1",
    }

# ---------- SEND / RECV ----------
def cmd_send(args):
    pad_path = Path(args.pad)
    in_path  = Path(args.infile)
    out_path = Path(args.outfile)
    meta_path = out_path.with_suffix(out_path.suffix + ".meta.json")

    # lade input
    M = in_path.read_bytes()
    L = len(M)

    # reserviere Pad: [Kenc | r | K2]
    need = L + R_LEN + TAG_LEN
    off_enc = reserve_pad(pad_path, need)
    off_r   = off_enc + L
    off_k2  = off_r + R_LEN

    info = load_pad_info(pad_path)
    pad_id = info["pad_id"]

    Kenc = read_pad_slice(pad_path, off_enc, L)
    r    = read_pad_slice(pad_path, off_r, R_LEN)
    K2   = read_pad_slice(pad_path, off_k2, TAG_LEN)

    # Ciphertext
    C = xor_bytes(M, Kenc)

    # WC-MAC: Tag = H_r(M) XOR K2
    H = poly_hash_mod_p(M, r)
    H_bytes = int_to_le(H, TAG_LEN)  # 16-Byte repr
    T = xor_bytes(H_bytes, K2)

    # schreibe CT+Tag
    out_path.write_bytes(C + T)

    # schreibe Meta (Header)
    hdr = build_header(PAD_STATE_VERSION, pad_id, off_enc, off_r, off_k2, L)
    meta_path.write_text(json.dumps(hdr, indent=2), encoding="utf-8")

    print(f"[SEND] wrote {out_path} (+ {meta_path}), len={L}, pad_id={pad_id}")
    print(f"[PAD ] used [{off_enc}:{off_enc+need}) total={need} bytes")

def cmd_recv(args):
    pad_path = Path(args.pad)
    in_path  = Path(args.infile)   # erwartet: C || T
    meta_path = Path(args.meta)    # header JSON
    out_path = Path(args.outfile)

    hdr = json.loads(meta_path.read_text(encoding="utf-8"))
    if hdr.get("enc") != "OTP+WC" or hdr.get("version") != PAD_STATE_VERSION:
        raise SystemExit("[ERR] Unbekanntes/inkompatibles Header-Format.")

    L = int(hdr["len"])
    off_enc = int(hdr["offset_enc"])
    off_r   = int(hdr["offset_r"])
    off_k2  = int(hdr["offset_k2"])
    tag_len = int(hdr["tag_len"])
    r_len   = int(hdr["r_len"])

    data = in_path.read_bytes()
    if len(data) < L + tag_len:
        raise SystemExit("[ERR] Eingabedatei zu kurz.")
    C = data[:L]
    T = data[L:L+tag_len]

    # Lade Pad-Slices
    Kenc = read_pad_slice(pad_path, off_enc, L)
    r    = read_pad_slice(pad_path, off_r, r_len)
    K2   = read_pad_slice(pad_path, off_k2, tag_len)

    # MAC prüfen
    M_tmp = xor_bytes(C, Kenc)  # Kandidaten-Klartext
    H = poly_hash_mod_p(M_tmp, r)
    H_bytes = int_to_le(H, tag_len)
    T_check = xor_bytes(H_bytes, K2)
    if not (T_check == T):
        raise SystemExit("[ERR] MAC-Prüfung fehlgeschlagen (manipulierte Daten oder falsches Pad).")

    # OK → schreibe Klartext
    out_path.write_bytes(M_tmp)
    print(f"[RECV] wrote {out_path} (len={L})")
    print("[OK]  MAC verifiziert, OTP entschlüsselt.")

# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="One-Time-Pad + Wegman-Carter-MAC (polynomial hash).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("send", help="Nachricht verschlüsseln + MAC")
    s.add_argument("--pad", required=True, help="Pfad zur Pad-Datei (binär).")
    s.add_argument("--infile", required=True, help="Klartext-Datei.")
    s.add_argument("--outfile", required=True, help="Zieldatei (Ciphertext+Tag).")
    s.set_defaults(func=cmd_send)

    r = sub.add_parser("recv", help="Nachricht entschlüsseln + MAC prüfen")
    r.add_argument("--pad", required=True, help="Pfad zur Pad-Datei (binär).")
    r.add_argument("--infile", required=True, help="Ciphertext+Tag-Datei (von send).")
    r.add_argument("--meta", required=True, help="Meta-JSON (von send).")
    r.add_argument("--outfile", required=True, help="Zieldatei (Klartext).")
    r.set_defaults(func=cmd_recv)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
