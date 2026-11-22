# opendm40 v0.4.1 中文版（zh12）源码

这是 **v0.4.1-zh12 的完整固件源码**，可以直接构建出 Release 里的
`opendm40-v0.4.1-zh.bin`（634,240 字节，CRC-32 `bd941428`，
SHA-256 `c1a54fc8…4819f87eb`）。

- 上游：<https://github.com/opendm40/opendm40>（MIT）
- 汉化与改动：本项目；许可证见 [LICENSE](LICENSE)（MIT，保留上游版权）
- 本目录只含**固件、构建脚本和字体工具**；上游的 `hw/`、`emu/`、`docs/`、
  `toolchain/` 等请从上游 v0.4.1 获取。

## 目录

```
firmware/
  src/                 固件源码（汉化与功能改动都在这里）
  vendor/usbd-storage/ 打了 5 个补丁的依赖（Cargo [patch.crates-io]）
  Cargo.toml / Cargo.lock
  build.rs / build.sh / link-native.x / .cargo/config.toml
  tools/fw-version.sh、tools/stack-depth/stackdepth.py
stock/dm40fw.py        原厂更新文件打包/解包工具（build.sh 调用）
font-tools/            汉字子集生成与 TEXT22/F14 字体重建
build-zh12.sh          构建入口（设置环境后调用 firmware/build.sh）
```

## 构建

需要：

- Rust stable（开发时用 1.99.1）：
  `rustup target add thumbv7em-none-eabihf`，
  `rustup component add llvm-tools rust-src`
- Python 3（`python3` 在 PATH；`dm40fw.py`、`stackdepth.py` 和 build.sh 的内联 Python 用）
- bash / git-bash（Windows）
- 首次构建需要网络让 Cargo 取依赖；已有 Cargo 缓存时可 `--offline`

```bash
cd source/opendm40-v0.4.1-zh12
./build-zh12.sh
# 或：./build-zh12.sh --offline
```

Windows 用 git-bash 执行同一个脚本。脚本会处理 `RUSTUP_HOME` / `CARGO_HOME`
的 Windows/MSYS 路径差异，并把 rustup 的 llvm-tools 目录加进 PATH
（`stackdepth.py` 需要 `llvm-objdump`）。

产物：

- `firmware/opendm40.bin`
- `firmware/dm40_opendm40_v0.4.1.bin`（原厂更新格式，可刷机）

构建末尾会打印 `region A2 free / B free / C free`；B 区非常紧，改动文案/字体前先看
[开发记录](../../docs/开发记录.md) 里的空间说明。

## 字体（改中文文案时）

源码里已经带了生成好的 `firmware/src/stockfont_data.rs`，**普通构建不需要重跑字体**。
新增/修改中文界面文字后，必须重生成字体，否则新字显示空白：

```bash
cd font-tools
python3 derive_sets.py stock_cjk_set.txt ../firmware/src/*.rs
python3 rebuild_fonts.py \
  --pristine pristine-stockfont_data.rs \
  --cjk-src cjk-src/stockfont_data.rs \
  --out ../firmware/src/stockfont_data.rs \
  --txt22-keep keep_cjk.txt --txt22-draw need_glyphs.txt --cjk-px 17
```

- 需要 Pillow 和宋体 `simsun.ttc`（脚本里是 Windows 路径
  `C:\Windows\Fonts\simsun.ttc`，其他系统请改 `TTF`）。
- 汉字统一走 **TEXT22**（22 px 字格、17 px 渲染）。F14 / F21 / SC_F12 / SC_F16 /
  ASCII26 画汉字会空白或乱码；`Tb` 字节缓冲也不能直接放 UTF-8 汉字。
- 本版 F14 没有汉字字形，所以重建命令**不加 `--f14`**；给 F14 加字没有意义。
- 字库占 B 区空间，一个 17 px 汉字约 47 字节；加字前先确认 `region B free`。

## 汉化改动在哪里

主要文件：

| 文件 | 内容 |
|---|---|
| `firmware/src/stockfont_data.rs` | 生成的中文 TEXT22 字库（含补字） |
| `firmware/src/ui.rs` | 设置/量程/限值/记录/速率 chip/状态栏徽标 |
| `firmware/src/sentinel.rs` | 告警徽标与红色提示弹窗文案 |
| `firmware/src/app.rs` | 设置存储、暗屏/关机、记录页、toast |
| `firmware/src/ui_power.rs` | 功率设置页、接线弹窗 |
| `firmware/src/dialog.rs` | 白色/红色弹窗与中文居中 |
| `firmware/src/ui_decode.rs`、`scope_ui.rs` | 示波器与解码页 |

更多设计取舍见仓库的 [开发记录](../../docs/开发记录.md)、[更新记录](../../CHANGELOG.md)
和 [README](../../README.md)。

## 许可证

MIT。上游版权归 opendm40 contributors；汉化与功能改动版权归
xingyan4117-sketch。见 [LICENSE](LICENSE)。
