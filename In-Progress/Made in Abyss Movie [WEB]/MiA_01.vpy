import vapoursynth as vs
from vapoursynth import core
import fvsfunc as fvf
import havsfunc as haf
import kagefunc as kgf
import n4ofunc as nao
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2
from vsutil import insert_clip, iterate, get_y, get_w

core.max_cache_size = 5250

src_a = nao.src(r"D:\kresbay nitip\_Fansub\Source\MiA_Movie\Made in Abyss - Movie 01 (Wakanim RU 1080p).mkv", depth=16)
src_a = src_a[:170880]

src_b = nao.src(r"D:\kresbay nitip\_Fansub\Source\MiA_Movie\Made in Abyss - Movie 01 (Wakanim SC 1080p).mkv", depth=16)
src_b = src_b[:170880]

src_c = nao.src(r"D:\kresbay nitip\_Fansub\Source\MiA_Movie\Made in Abyss - Movie 01 (Amazon dAnime VBR 720p).mkv", depth=16)
src_c = src_c[:170880]
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

#Manual masking (capek asu)
src = insert_clip(src, src_fade2[170580:170712], 170580)
src = insert_clip(src, src_fade2[167470:167603], 167470)
src = insert_clip(src, src_fade2[152854:152953], 152854)
src = insert_clip(src, src_fade2[89587:89689], 89587)
src = insert_clip(src, src_fade2[83796:83889], 83796)
src = insert_clip(src, src_fade2[73893:74065], 73893)
src = insert_clip(src, src_fade2[46296:46357], 46296)
src = insert_clip(src, src_fade2[5818:5910], 5818)
src = insert_clip(src, src_fade2[3041:3202], 3201)

src = nao.rapplym(src, src_fade2, r"D:\kresbay nitip\_Encode\Skrip\mia\masks\01")

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