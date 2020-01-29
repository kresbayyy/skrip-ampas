import vapoursynth as vs
core = vs.get_core()
import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf
import kagefunc as kgf
import n4ofunc as nao
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import iterate, get_y, get_w

core.max_cache_size = 4000

src = nao.src(r"E:\BDMV\キャロル＆チューズデイ Blu-ray Disc BOX Vol.1\DISC1\BDMV\STREAM\00004.m2ts", depth=16)
src = core.edgefixer.ContinuityFixer(src, 1, 1, 1, 1, 2)
src = src[:32847+1]

descaled = fvf.Debicubic(src, 1280, 720, b=0, c=1, yuv444=True)

sobel_edge = iterate(core.std.Sobel(get_y(descaled)), core.std.Inflate, 2)
normal_deband = core.f3kdb.Deband(descaled, 12, 60, 45, 45, 15, 0, output_depth=16)

sobel = core.std.MaskedMerge(descaled, normal_deband, sobel_edge)

vid = core.dfttest.DFTTest(sobel, sigma=0.5, tbsize=1, sbsize=24, sosize=18)
#vid = nao.adaptive_smdegrain(vid, luma_scaling=10, iter_edge=1, thSAD=190, thSADC=150)
vid = taa.TAAmbk(vid, "Nnedi3", cycle=2)
vid = kgf.adaptive_grain(vid, 0.15, luma_scaling=16)
vid = fvf.Depth(vid, 16)

vid.set_output()