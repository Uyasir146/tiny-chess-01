import json, os, ssl, time, urllib.request, urllib.error
from random import Random
MATE = 100000
NODES = 140000
SEEN = {}
CT = 25
KN = (-33, -31, -18, -14, 14, 18, 31, 33)
BI = (-17, -15, 15, 17)
RO = (-16, -1, 1, 16)
KI = (-17, -16, -15, -1, 1, 15, 16, 17)
VAL = {"p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 0}
AT = (((BI, "bq"), (RO, "rq")), ((BI, "BQ"), (RO, "RQ")))
def tb(s):
  o = []
  for r in range(0, 32, 4):
    v = [(ord(c) - 60) * 5 for c in s[r:r + 4]]
    o += v + v[::-1]
  return o
PM = tb("<<<<=>>8=;:<<<<@==>A>>@BFFFF<<<<")
NM = tb("246648<=6<>?6=?@6<?@6=>?48<<2466")
BM = tb("8::::=<<:>>>:<>>:==>:<=>:<<<8:::")
RM = tb("<<<=;<<<;<<<;<<<;<<<;<<<=>>><<<<")
QM = tb("8::;:<<<:<==;<==;<==:<==:<<<8::;")
KM = tb("@B><@@<<:88886646442644264426442")
KE = tb("266666<<6:@B6:BD6:BD6:@B68:<2468")
TB = {"p": PM, "n": NM, "b": BM, "r": RM, "q": QM, "k": KM}
CRL = [15] * 128
CRL[4] = 12
CRL[0] = 13
CRL[7] = 14
CRL[116] = 3
CRL[112] = 7
CRL[119] = 11
_r = Random(20261117)
Z = {c: [_r.getrandbits(64) for _ in range(128)] for c in "PNBRQKpnbrqk"}
ZS = _r.getrandbits(64)
ZCR = [_r.getrandbits(64) for _ in range(16)]
ZEP = [_r.getrandbits(64) for _ in range(128)]
class P:
  def __init__(self, fen):
    f = fen.split()
    b = self.b = {}
    q = 0
    for c in f[0]:
      if c.isdigit():
        q += int(c)
      elif c != "/":
        b[(7 - (q >> 3)) * 16 + (q & 7)] = c
        q += 1
    self.side = 1 if f[1] == "w" else -1
    self.cr = 0 if f[2] == "-" else sum(2 ** "KQkq".index(c) for c in f[2])
    self.ep = -1 if f[3] == "-" else (int(f[3][1]) - 1) * 16 + "abcdefgh".index(f[3][0])
    self.hm = int(f[4]) if len(f) > 4 else 0
    ks = self.ks = {}
    h = 0
    for s, p in b.items():
      h ^= Z[p][s]
      if p in "Kk":
        ks[1 if p == "K" else -1] = s
    if self.side < 0:
      h ^= ZS
    h ^= ZCR[self.cr]
    if self.ep >= 0:
      h ^= ZEP[self.ep]
    self.h = h
    self.rep = dict(SEEN)
    SEEN[h] = self.rep[h] = SEEN.get(h, 0) + 1
    self.tt = {}
    self.kill = {}
    self.hist = {}
    self.nodes = 0
    self.budget = NODES
    self.stop = False
    self.und = []
    self.bm = None
  def atk(self, s, sd):
    b = self.b
    d = 16 if sd > 0 else -16
    for o in (-d - 1, -d + 1):
      t = s + o
      if not t & 0x88 and b.get(t) == ("P" if sd > 0 else "p"):
        return True
    for os_, pc in ((KN, "N"), (KI, "K")):
      pc = pc if sd > 0 else pc.lower()
      for o in os_:
        t = s + o
        if not t & 0x88 and b.get(t) == pc:
          return True
    for os_, ps in AT[sd > 0]:
      for o in os_:
        t = s + o
        while not t & 0x88:
          v = b.get(t)
          if v:
            if v in ps:
              return True
            break
          t += o
    return False
  def gen(self, ttm, allm):
    b = self.b
    w = self.side > 0
    out = []
    a = out.append
    pro = "QRBN" if w else "qrbn"
    for q, p in b.items():
      if p.isupper() != w:
        continue
      lo = p.lower()
      if lo == "p":
        d = 16 if w else -16
        o = q + d
        ts = []
        if not o & 0x88 and o not in b:
          ts.append(o)
          t = q + 2 * d
          if not t & 0x88 and t not in b and q >> 4 == (1 if w else 6):
            ts.append(t)
        for e in (-1, 1):
          t = o + e
          if t & 0x88 or (t & 7) - (q & 7) != e:
            continue
          v = b.get(t)
          if v and v.isupper() != w or t == self.ep:
            ts.append(t)
        for t in ts:
          if t >> 4 in (0, 7):
            for r in pro:
              a((q, t, r))
          else:
            a((q, t, ""))
      elif lo == "n" or lo == "k":
        for r in KN if lo == "n" else KI:
          t = q + r
          if not t & 0x88:
            v = b.get(t)
            if not v:
              if allm:
                a((q, t, ""))
            elif v.isupper() != w:
              a((q, t, ""))
      else:
        for r in BI if lo == "b" else RO if lo == "r" else KI:
          t = q + r
          while not t & 0x88:
            v = b.get(t)
            if v:
              if v.isupper() != w:
                a((q, t, ""))
              break
            if allm:
              a((q, t, ""))
            t += r
    kq = 4 if w else 116
    if b.get(kq) == ("K" if w else "k"):
      for kt, bit in (((6, 1), (2, 2)) if w else ((118, 4), (114, 8))):
        rf = kq + 3 if kt > kq else kq - 4
        if (self.cr & bit and b.get(rf) == ("R" if w else "r")
            and not any(b.get(x) for x in range(min(kq, rf) + 1, max(kq, rf)))
            and not self.atk(kq, -self.side)
            and not self.atk((kq + kt) >> 1, -self.side)
            and not self.atk(kt, -self.side)):
          a((kq, kt, ""))
    return out
  def order(self, ms, ttm, allm, ply):
    b = self.b
    k = self.kill.get(ply, ())
    out = []
    for m in ms:
      f, t, pr = m
      v = b.get(t)
      if m == ttm:
        s = 2e6
      elif v and v.isupper() != b[f].isupper():
        s = 1e6 + 10 * VAL[v.lower()] - VAL[b[f].lower()]
      elif pr:
        s = 9e5
      elif m in k:
        s = 8e5
      elif allm:
        s = self.hist.get((b[f], t), 0)
      else:
        continue
      out.append((s, m))
    out.sort(reverse=True)
    return out
  def mk(self, m):
    b = self.b
    f, t, pr = m
    pc = b[f]
    h = self.h
    cap = b.get(t, ".")
    cs = -1
    if pc in "Pp" and t == self.ep and (t & 7) != (f & 7):
      cs = t - 16 * self.side
      cap = b[cs]
    self.und.append((m, cap, cs, self.cr, self.ep, self.hm, h))
    h ^= Z[pc][f]
    if cs >= 0:
      del b[cs]
      h ^= Z[cap][cs]
    elif cap != ".":
      h ^= Z[cap][t]
    del b[f]
    np = (pr.upper() if pc.isupper() else pr.lower()) if pr else pc
    b[t] = np
    h ^= Z[np][t]
    if pc in "Kk":
      self.ks[self.side] = t
      if abs(t - f) == 2:
        rf = t + 1 if t > f else t - 2
        rt = t - 1 if t > f else t + 1
        rp = b.pop(rf)
        b[rt] = rp
        h ^= Z[rp][rf] ^ Z[rp][rt]
    cr = self.cr & CRL[f] & CRL[t]
    if self.ep >= 0:
      h ^= ZEP[self.ep]
    self.ep = (f + t) >> 1 if pc in "Pp" and abs(t - f) == 32 else -1
    if self.ep >= 0:
      h ^= ZEP[self.ep]
    h ^= ZCR[self.cr] ^ ZCR[cr] ^ ZS
    self.cr = cr
    self.hm = 0 if (pc in "Pp" or cap != ".") else self.hm + 1
    self.h = h
    self.side = -self.side
    self.rep[h] = self.rep.get(h, 0) + 1
  def un(self):
    m, cap, cs, cr, ep, hm, h = self.und.pop()
    b = self.b
    f, t, pr = m
    self.side = -self.side
    self.rep[self.h] -= 1
    pc = b.pop(t)
    if pr:
      pc = "P" if self.side > 0 else "p"
    b[f] = pc
    if cs >= 0:
      b[cs] = cap
    elif cap != ".":
      b[t] = cap
    if pc in "Kk":
      self.ks[self.side] = f
      if abs(t - f) == 2:
        rf = t + 1 if t > f else t - 2
        rt = t - 1 if t > f else t + 1
        b[rf] = b.pop(rt)
    self.cr = cr
    self.ep = ep
    self.hm = hm
    self.h = h
  def ev(self):
    b = self.b
    n = len(b)
    r = 0
    wb = bb = 0
    for q, p in b.items():
      lo = p.lower()
      w = p.isupper()
      i = (q & 7) + (q >> 4) * 8 if w else (q & 7) + (7 - (q >> 4)) * 8
      m = VAL[lo] + (KE[i] if lo == "k" and n < 14 else TB[lo][i])
      r += m if w else -m
      if lo == "b":
        if w:
          wb += 1
        else:
          bb += 1
    if wb > 1:
      r += 32
    if bb > 1:
      r -= 32
    return (r if self.side > 0 else -r) + 8
  def ab(self, d, al, be, ply):
    b = self.b
    self.nodes += 1
    if self.nodes > self.budget:
      self.stop = True
      return 0
    if self.stop:
      return 0
    chk = self.atk(self.ks[self.side], -self.side)
    if chk and d > 0 and ply < 30:
      d += 1
    ttm = None
    if d > 0:
      if ply and (self.hm > 99 or self.rep.get(self.h, 0) > 1):
        return 0
      if ply:
        e = self.tt.get(self.h)
        if e:
          ed, ef, es, ttm = e
          if ed >= d and (ef == 0 or (ef == 1 and es >= be) or (ef == 2 and es <= al)):
            return es
      else:
        ttm = self.bm
      if d > 2 and ply and not chk and len(b) > 12 and be < MATE - 200:
        o = self.ep
        self.h ^= ZS ^ (ZEP[o] if o >= 0 else 0)
        self.side = -self.side
        self.ep = -1
        self.hm += 1
        v = -self.ab(d - 3, -be, -be + 1, ply + 1)
        self.hm -= 1
        self.ep = o
        self.h ^= ZS ^ (ZEP[o] if o >= 0 else 0)
        self.side = -self.side
        if self.stop:
          return 0
        if v >= be:
          return be
    elif not chk:
      v = self.ev()
      if v >= be:
        return be
      if v > al:
        al = v
      if ply > 32:
        return al
    a0 = al
    allm = d > 0 or chk
    ms = self.order(self.gen(ttm, allm), ttm, allm, ply)
    best = al if d <= 0 else -MATE
    bm = None
    n = 0
    alt = None
    for sc, m in ms:
      f, t, pr = m
      quiet = not pr and t not in b and not (b[f] in "Pp" and t == self.ep)
      self.mk(m)
      if self.atk(self.ks[-self.side], self.side):
        self.un()
        continue
      if not ply and self.rep.get(self.h, 0) > 1 and self.ev() > -80:
        alt = m
        self.un()
        continue
      n += 1
      if n == 1:
        v = -self.ab(d - 1, -be, -al, ply + 1)
      else:
        r = 2 if (d > 3 and n > 6 and quiet and not chk) else (1 if (d > 2 and n > 3 and quiet and not chk) else 0)
        v = -self.ab(d - 1 - r, -al - 1, -al, ply + 1)
        if v > al and (r or v < be):
          v = -self.ab(d - 1, -be, -al, ply + 1)
      self.un()
      if self.stop:
        return 0
      if v > best:
        best = v
        bm = m
        if not ply:
          self.bm = m
        if v > al:
          al = v
          if al >= be:
            if quiet:
              kk = self.kill.get(ply, ())
              if m not in kk:
                self.kill[ply] = (m,) + kk[:1]
              self.hist[(b[f], t)] = self.hist.get((b[f], t), 0) + d * d
            break
    if not n:
      if alt is not None:
        self.bm = alt
        return 0
      return -MATE + ply if chk else (best if d <= 0 else 0)
    if d > 0 and ply and bm:
      self.tt[self.h] = (d, 2 if best <= a0 else (1 if best >= be else 0), best, bm)
    return best
  def search(self):
    self.tt = {}
    self.kill = {}
    self.hist = {}
    self.nodes = 0
    self.stop = False
    self.bm = None
    best = None
    pv = 0
    for d in range(1, 60):
      self.bm = best
      w = None if d < 4 else 50
      while True:
        if w is None:
          al, be = -MATE, MATE
        else:
          al, be = pv - w, pv + w
        v = self.ab(d, al, be, 0)
        if self.stop:
          break
        if w is not None and (v <= al or v >= be):
          w = w * 6 if w < 300 else None
          continue
        pv = v
        break
      if self.bm:
        best = self.bm
      if self.stop or v > MATE - 200:
        break
    return best
EU = (os.environ.get("MAKEFUN_ENV_URL") or "").strip().rstrip("/")
CAND = ([EU] if EU else []) + ["http://" + h + ":" + str(p)
                 for p in (8080, 8000, 3000, 5000, 8123)
                 for h in ("127.0.0.1", "localhost")]
OP = urllib.request.build_opener(
  urllib.request.HTTPSHandler(context=ssl._create_unverified_context()))
def post(p, o):
  body = json.dumps(o).encode()
  hd = {"content-type": "application/json"}
  r = {} if p == "/game" else {"status": "again"}
  for k in range(3000):
    for c in CAND:
      try:
        return json.load(OP.open(urllib.request.Request(c + p, body, hd), timeout=10))
      except urllib.error.HTTPError as e:
        if 400 <= e.code < 500:
          return {} if p == "/game" else {"status": "again"}
      except Exception:
        pass
    time.sleep(min(0.1 * (k + 1), 1.0))
  return r
def uci(m):
  return ("abcdefgh"[m[0] & 7] + str((m[0] >> 4) + 1) +
      "abcdefgh"[m[1] & 7] + str((m[1] >> 4) + 1) + (m[2] or "").lower())
def main():
  gid = None
  while True:
    g = post("/game", {})
    if not isinstance(g, dict):
      g = {}
    if g.get("status") == "done":
      return
    if g.get("status") != "your_move":
      time.sleep(0.05)
      continue
    while g.get("status") == "your_move":
      if g.get("game") != gid:
        SEEN.clear()
        gid = g.get("game")
      lm = g.get("legal_moves") or []
      mv = lm[0] if lm else None
      try:
        m = P(g["fen"]).search()
        if m and (not lm or uci(m) in lm):
          mv = uci(m)
      except Exception:
        pass
      if mv is None:
        return
      g = post("/move", {"game": g.get("game"), "move": mv})
      if not isinstance(g, dict):
        g = {}
main()
