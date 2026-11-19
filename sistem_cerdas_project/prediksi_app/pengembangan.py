import base64
import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
FALLBACK_CSV_URL = (
    "https://raw.githubusercontent.com/rahmadhaninadhin-ctrl/"
    "nilai_mahasiswa/main/SmartPhone.csv"
)

WARNA_BG = "#fffdf9"
WARNA_TEKS = "#2b2118"
WARNA_LEMBUT = "#635345"
WARNA_GRID = "#e5d8c3"
WARNA_SAGE = "#3f6254"
WARNA_TERRACOTTA = "#c85a32"


def _terapkan_gaya_grafik(ax, grid_axis: str = "y") -> None:
    ax.set_facecolor(WARNA_BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cfc0a8")
    ax.spines["bottom"].set_color("#cfc0a8")
    ax.tick_params(colors=WARNA_LEMBUT, labelsize=9)
    ax.xaxis.label.set_color(WARNA_LEMBUT)
    ax.yaxis.label.set_color(WARNA_LEMBUT)
    ax.title.set_color(WARNA_TEKS)
    ax.set_axisbelow(True)
    ax.grid(
        axis=grid_axis,
        linestyle="--",
        linewidth=0.75,
        color=WARNA_GRID,
        alpha=0.95,
    )


def _fig_to_base64(fig) -> str:
    buffer = io.BytesIO()
    fig.tight_layout()
    fig.savefig(
        buffer,
        format="png",
        dpi=120,
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _pilih_sumber_csv():
    kandidat_lokal = [
        BASE_DIR / "Smartphone.csv",
        BASE_DIR / "SmartPhone.csv",
        Path(__file__).resolve().parent / "Smartphone.csv",
        Path(__file__).resolve().parent / "SmartPhone.csv",
    ]
    for path in kandidat_lokal:
        if path.exists():
            return path
    return FALLBACK_CSV_URL


def _baca_csv_aman(sumber_data) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            df = pd.read_csv(sumber_data, encoding=enc)
            df.columns = [str(col).strip() for col in df.columns]
            if not df.empty or len(df.columns) > 0:
                return df
        except Exception:
            continue
    df = pd.read_csv(sumber_data)
    df.columns = [str(col).strip() for col in df.columns]
    return df


def hitung_diskon_numpy(
    harga_asli_list: list[float] | None = None,
    harga_diskon_list: list[float] | None = None,
) -> dict:
    if not harga_asli_list or not harga_diskon_list:
        harga_asli = np.array(
            [2500000, 3200000, 1800000, 4500000, 1500000], dtype=float
        )
        harga_diskon = np.array(
            [2100000, 2700000, 1500000, 3900000, 1250000], dtype=float
        )
    else:
        harga_asli = np.array(harga_asli_list, dtype=float)
        harga_diskon = np.array(harga_diskon_list, dtype=float)

    if (
        harga_asli.size == 0
        or harga_diskon.size == 0
        or harga_asli.size != harga_diskon.size
    ):
        raise ValueError(
            "Jumlah data harga asli dan harga diskon harus sama dan tidak boleh kosong."
        )

    besar_diskon = harga_asli - harga_diskon

    rincian = [
        {
            "no": idx + 1,
            "harga_asli": float(asli),
            "harga_diskon": float(diskon),
            "besar_diskon": float(selisih),
        }
        for idx, (asli, diskon, selisih) in enumerate(
            zip(harga_asli, harga_diskon, besar_diskon)
        )
    ]

    return {
        "rincian": rincian,
        "rata_rata": float(np.mean(besar_diskon)),
        "maksimum": float(np.max(besar_diskon)),
        "minimum": float(np.min(besar_diskon)),
        "teks_asli": ", ".join(
            str(int(x)) if float(x).is_integer() else str(x) for x in harga_asli
        ),
        "teks_diskon": ", ".join(
            str(int(x)) if float(x).is_integer() else str(x) for x in harga_diskon
        ),
    }


def jalankan_pengembangan_smartphone() -> dict:
    sumber_data = _pilih_sumber_csv()
    df = _baca_csv_aman(sumber_data)

    # Tentukan kolom acuan harga & RAM secara otomatis
    if "harga_juta" in df.columns:
        df["harga_acuan"] = pd.to_numeric(df["harga_juta"], errors="coerce")
        label_harga = "harga_juta"
    elif "discounted_price" in df.columns:
        df["harga_acuan"] = pd.to_numeric(df["discounted_price"], errors="coerce")
        label_harga = "discounted_price"
    elif "original_price" in df.columns:
        df["harga_acuan"] = pd.to_numeric(df["original_price"], errors="coerce")
        label_harga = "original_price"
    else:
        df["harga_acuan"] = np.nan
        label_harga = "harga"

    if "ram_gb" in df.columns:
        df["ram_acuan"] = pd.to_numeric(df["ram_gb"], errors="coerce")
        label_ram = "ram_gb"
    elif "ram" in df.columns:
        df["ram_acuan"] = pd.to_numeric(df["ram"], errors="coerce")
        label_ram = "ram"
    else:
        df["ram_acuan"] = np.nan
        label_ram = "ram"

    # Rata-rata harga_acuan per ram_acuan
    rata_per_ram = []
    ram_grouped = (
        df.dropna(subset=["ram_acuan", "harga_acuan"])
        .groupby("ram_acuan", as_index=False)["harga_acuan"]
        .mean()
        .sort_values("ram_acuan", ascending=True)
    )
    if not ram_grouped.empty:
        rata_per_ram = [
            {
                "ram_gb": r["ram_acuan"],
                "label_ram": (
                    f"{int(r['ram_acuan'])} GB"
                    if float(r["ram_acuan"]).is_integer()
                    else f"{r['ram_acuan']} GB"
                ),
                "harga_juta": float(r["harga_acuan"]),
            }
            for _, r in ram_grouped.iterrows()
        ]

    # Filter produk dengan harga_acuan > rata-rata
    rata_harga = (
        float(df["harga_acuan"].mean())
        if df["harga_acuan"].notna().any()
        else None
    )
    if rata_harga is not None:
        df_di_atas_rata = df[df["harga_acuan"] > rata_harga].copy()
    else:
        df_di_atas_rata = df.copy()

    # 1. Histogram harga_acuan (jarak antarbatang rwidth=0.75)
    fig_hist, ax_hist = plt.subplots(figsize=(6, 4))
    fig_hist.patch.set_facecolor(WARNA_BG)
    data_hist = df["harga_acuan"].dropna()
    if not data_hist.empty:
        ax_hist.hist(
            data_hist,
            bins=min(8, max(3, len(data_hist))),
            rwidth=0.75,
            color=WARNA_SAGE,
            edgecolor=WARNA_BG,
            linewidth=1.1,
        )
        ax_hist.set_title("Distribusi Harga Smartphone", loc="left", fontweight="bold")
        ax_hist.set_xlabel(label_harga)
        ax_hist.set_ylabel("Jumlah Produk")
        _terapkan_gaya_grafik(ax_hist, grid_axis="y")
        catatan_hist = (
            f"Sebaran {len(data_hist)} produk (rata-rata {data_hist.mean():,.2f})."
        )
    else:
        ax_hist.text(0.5, 0.5, "Kolom harga tidak tersedia", ha="center", color=WARNA_TEKS)
        _terapkan_gaya_grafik(ax_hist, grid_axis="y")
        catatan_hist = "Data harga belum tersedia."
    grafik_hist = _fig_to_base64(fig_hist)

    # 2. Bar chart rata-rata harga per kapasitas RAM
    fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
    fig_bar.patch.set_facecolor(WARNA_BG)
    if rata_per_ram:
        ax_bar.bar(
            [r["label_ram"] for r in rata_per_ram],
            [r["harga_juta"] for r in rata_per_ram],
            width=0.52,
            color=WARNA_SAGE,
            edgecolor="none",
        )
        ax_bar.set_title("Rata-Rata Harga per Kapasitas RAM", loc="left", fontweight="bold")
        ax_bar.set_xlabel(label_ram)
        ax_bar.set_ylabel(f"Rata-Rata {label_harga}")
        _terapkan_gaya_grafik(ax_bar, grid_axis="y")
        catatan_bar = (
            f"Menampilkan rata-rata harga pada {len(rata_per_ram)} variasi RAM."
        )
    else:
        ax_bar.text(0.5, 0.5, "Data rata-rata per RAM kosong", ha="center", color=WARNA_TEKS)
        _terapkan_gaya_grafik(ax_bar, grid_axis="y")
        catatan_bar = "Data rata-rata per RAM belum tersedia."
    grafik_bar = _fig_to_base64(fig_bar)

    # 3. Scatter plot hubungan RAM dan harga
    fig_scat, ax_scat = plt.subplots(figsize=(6, 4))
    fig_scat.patch.set_facecolor(WARNA_BG)
    df_scatter = df.dropna(subset=["ram_acuan", "harga_acuan"])
    if not df_scatter.empty:
        ax_scat.scatter(
            df_scatter["ram_acuan"],
            df_scatter["harga_acuan"],
            s=55,
            color=WARNA_TERRACOTTA,
            edgecolors=WARNA_BG,
            linewidth=1.0,
            alpha=0.9,
        )
        ax_scat.set_title("Hubungan RAM dan Harga", loc="left", fontweight="bold")
        ax_scat.set_xlabel(label_ram)
        ax_scat.set_ylabel(label_harga)
        _terapkan_gaya_grafik(ax_scat, grid_axis="both")
        catatan_scatter = (
            f"Membandingkan {label_ram} dan {label_harga} pada {len(df_scatter)} data."
        )
    else:
        ax_scat.text(0.5, 0.5, "Kolom RAM / harga tidak valid", ha="center", color=WARNA_TEKS)
        _terapkan_gaya_grafik(ax_scat, grid_axis="both")
        catatan_scatter = "Kolom RAM atau harga tidak tersedia."
    grafik_scatter = _fig_to_base64(fig_scat)

    # Semua kolom asli dari CSV (maks. 20 baris)
    kolom_tampil = [
        str(c) for c in df.columns if c not in {"harga_acuan", "ram_acuan"}
    ]
    tabel_semua_data = (
        df[kolom_tampil].head(20).fillna("-").to_dict(orient="records")
        if kolom_tampil
        else []
    )
    tabel_di_atas_rata = (
        df_di_atas_rata[kolom_tampil].head(20).fillna("-").to_dict(orient="records")
        if kolom_tampil
        else []
    )

    return {
        "sumber_data": str(sumber_data),
        "total_baris": len(df),
        "rata_harga_juta": round(rata_harga, 2) if rata_harga is not None else None,
        "jumlah_di_atas_rata": len(df_di_atas_rata),
        "kolom_tabel": kolom_tampil,
        "tabel_semua_data": tabel_semua_data,
        "tabel_di_atas_rata": tabel_di_atas_rata,
        "rata_per_ram": rata_per_ram,
        "grafik_hist": grafik_hist,
        "catatan_hist": catatan_hist,
        "grafik_bar": grafik_bar,
        "catatan_bar": catatan_bar,
        "grafik_scatter": grafik_scatter,
        "catatan_scatter": catatan_scatter,
        "numpy_diskon": hitung_diskon_numpy(),
    }