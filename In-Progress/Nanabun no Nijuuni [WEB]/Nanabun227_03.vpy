import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import kagefunc as kgf
import n4ofunc as nao
import lvsfunc as lvf
import havsfunc as haf
from vsutil import *
from nnedi3_rpow2 import *
core = vs.core

core.max_cache_size = 4500

funi = nao.src(r"C:\Encode\[Source]\Nanabun\[HorribleSubs] Nanabun no Nijyuuni - 03 [1080p].mkv", depth=16)
waka = nao.src(r"C:\Encode\[Source]\Nanabun\227_03_EN_HD.mp4", depth=16)

waka = waka[0]+waka[:12700]+waka[12699]*5+waka[12700:34396]+waka[34396]+waka[34396:]
funi = funi[289:]
waka = fvf.rfs(waka, funi, f"[0 1]")
#funi = funi[1:12701]+funi[12706:34403]+funi[34404:34523]

src_mask1 = kgf.hardsubmask(waka, funi)
src_dialog = core.std.MaskedMerge(waka, funi, src_mask1)
src_mask2 = kgf.hardsubmask_fades(src_dialog, funi, highpass=1200)
src_full = core.std.MaskedMerge(src_dialog, funi, src_mask2)

src = src_full

"""
stacked1 = core.std.StackVertical([get_y(waka), get_y(funi)])
stacked2 = core.std.StackVertical([get_y(src), src_mask2])
stackstack = core.std.StackHorizontal([stacked1, stacked2])
stackstack = stackstack.resize.Spline16(1280,720)
stackstack.set_output()
"""

descale = nao.descale(src, get_w(900), 900, "bicubic", b=1/5, c=2/5, expandN=3)
descale = nnedi3_rpow2(descale, 2, width=1920, height=1080, nsize=4, nns=2)

deb = fvf.Depth(core.deblock.Deblock(descale, quant=18), 16)

sobel_edge = iterate(core.std.Sobel(get_y(deb)), core.std.Inflate, 2).std.Invert()
normal_deband = core.f3kdb.Deband(deb, 16, 45, 45, 35, 15, 0, preset="medium/nograin", output_depth=16)

vid = core.std.MaskedMerge(src, normal_deband, sobel_edge)
#vid = nao.adaptive_smdegrain(vid, luma_scaling=10, iter_edge=1, thSAD=100, thSADC=80)
vid = haf.EdgeCleaner(vid, strength=2, rmode=13, smode=1)
vid = kgf.adaptive_grain(vid, 0.35, luma_scaling=20)
vid = fvf.Depth(vid, 10)

vid.set_output()
