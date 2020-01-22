import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf
import kagefunc as kgf
import n4ofunc as nao
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import insert_clip, iterate, get_y, get_w

core.max_cache_size = 2500

src_a = nao.src(r"D:\kresbay nitip\_Fansub\Source\MiA_Movie\Made in Abyss - Movie 02 (Wakanim RU 1080p).mkv", depth=16)
src_a = src_a[:151968]

src_b = nao.src(r"D:\kresbay nitip\_Fansub\Source\MiA_Movie\Made in Abyss - Movie 02 (Wakanim SC 1080p).mkv", depth=16)
src_b = src_b[:151968]

src_c = nao.src(r"D:\kresbay nitip\_Fansub\Source\MiA_Movie\Made in Abyss - Movie 02 (Amazon dAnime VBR 720p).mkv", depth=16)
src_c = src_c[:151968]
src_c = nnedi3_rpow2(src_c, 2, width=1920, height=1080, nsize=4, nns=2)

#Dialog
hardsubmask = kgf.hardsubmask(src_a, src_b)
src = core.std.MaskedMerge(src_a, src_b, hardsubmask)
hardsubmask_fade = fvf.Depth(kgf.hardsubmask_fades(src, src_b, highpass=3500), 16)
src_fade = core.std.MaskedMerge(src, src_b, hardsubmask_fade)

#TS
hardsubmask2 = kgf.hardsubmask(src_b, src_c)
src2 = core.std.MaskedMerge(src_b, src_c, hardsubmask2)
hardsubmask_fade2 = fvf.Depth(kgf.hardsubmask_fades(src2, src_c, highpass=3500), 16)
src_fade2 = core.std.MaskedMerge(src2, src_c, hardsubmask_fade2)

#Manual Masking Part 2 - ANJING CAPEK GUA
src = insert_clip(src, src_fade2[143050:143129], 143050)
src = insert_clip(src, src_fade2[142054:142133], 142054)
src = insert_clip(src, src_fade2[141928:141995], 141928)
src = insert_clip(src, src_fade2[141311:141365], 141311)
src = insert_clip(src, src_fade2[140830:140885], 140830)
src = insert_clip(src, src_fade2[140269:140336], 140269)
src = insert_clip(src, src_fade2[124402:124461], 124402)
src = insert_clip(src, src_fade2[91750:91830], 91750)
src = insert_clip(src, src_fade[58340:58409], 58340)
src = insert_clip(src, src_fade2[12031:12128], 12031)
src = insert_clip(src, src_fade2[3135:3250], 3135)
src = insert_clip(src, src_fade2[2062:2206], 2062)

src = nao.rapplym(src, src_fade2, r"D:\kresbay nitip\_Encode\Skrip\mia\masks\02")

descaled = nao.descale(src, get_w(900), 900, "lanczos", taps=5, expandN=3)
descaled = nnedi3_rpow2(descaled, 2, width=1920, height=1080, nsize=4, nns=2)

sobel_edge = iterate(core.std.Sobel(get_y(descaled)), core.std.Inflate, 2)
normal_deband = core.f3kdb.Deband(descaled, 14, 60, 45, 35, 15, 0, output_depth=16)

vid = core.std.MaskedMerge(descaled, normal_deband, sobel_edge)
vid = nao.adaptive_smdegrain(vid, luma_scaling=10, iter_edge=1, thSAD=190, thSADC=150)
vid = kgf.adaptive_grain(vid, 0.35, luma_scaling=16)
vid = taa.TAAmbk(vid, "Nnedi3", cycle=2)
vid = fvf.Depth(vid, 10)

vid.set_output()