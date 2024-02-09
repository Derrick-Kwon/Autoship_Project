import math
RE = 6371.00877 # earth diameter(km)
GRID = 5.0      # grid width(km)
SLAT1 = 30.0    # latitude1(degree)
SLAT2 = 60.0    # latitude2(degree)
OLON = 126.0    # 0point longitude(degree)
OLAT = 38.0     # 0point latitude(degree)
XO = 43         # 0point Xgrid(GRID)
YO = 136        # 0point Ygrid(GRID)

# LCC DFS 좌표변환 ( code : "toXY"(위경도->좌표, v1:위도, v2:경도), "toLL"(좌표->위경도,v1:x, v2:y) )
def dfs_xy_conv(code, v1, v2):
  DEGRAD = math.pi / 180.0
  RADDEG = 180.0 / math.pi

  re = RE / GRID
  slat1 = SLAT1 * DEGRAD
  slat2 = SLAT2 * DEGRAD
  olon = OLON * DEGRAD
  olat = OLAT * DEGRAD

  sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
  sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
  sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
  sf = math.pow(sf, sn) * math.cos(slat1) / sn
  ro = math.tan(math.pi * 0.25 + olat * 0.5)
  ro = re * sf / math.pow(ro, sn)
  rs = {}
  if (code == "toXY"):
    rs['lat'] = v1
    rs['lng'] = v2
    ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = v2 * DEGRAD - olon
    if (theta > math.pi): theta -= 2.0 * math.pi
    if (theta < -math.pi): theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
  else:
    rs['x'] = v1
    rs['y'] = v2
    xn = v1 - XO
    yn = ro - v2 + YO
    ra = math.sqrt(xn * xn + yn * yn)
    if (sn < 0.0): - ra
    alat = math.pow((re * sf / ra), (1.0 / sn))
    alat = 2.0 * math.atan(alat) - math.pi * 0.5

    if (math.abs(xn) <= 0.0):
      theta = 0.0
    else:
        if (math.abs(yn) <= 0.0):
            theta = math.pi * 0.5
            if (xn < 0.0): - theta
        else: theta = math.atan2(xn, yn)
    alon = theta / sn + olon
    rs['lat'] = alat * RADDEG
    rs['lng'] = alon * RADDEG
  return rs