プリンターでスキャンした画像をPDFに変換するツールです。

venvなどでPillow, img2pdf, numpy, opencv-pythonをインストールしてください。

以下、処理の流れです。
1. プリンターでTIFF形式で読み込みます。これにより高画質で取り込むことができます。
2. tiff2png.pyで画像をPNGに変換します。加工中はPNGで操作します。
3. modify.pyで縁取りやノイズ除去を行います。
4. 最後に、png2dtcpdf.pyによってPNGからjpeg埋め込みのPDFを作成します。
