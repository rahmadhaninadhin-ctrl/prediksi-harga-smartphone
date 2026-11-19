from django.http import JsonResponse
from django.shortcuts import render
from .pengembangan import hitung_diskon_numpy, jalankan_pengembangan_smartphone


def _parse_angka(teks: str) -> list[float]:
    bagian = [item.strip() for item in teks.split(",") if item.strip()]
    return [float(item) for item in bagian] if bagian else []


def index(request):
    konteks = {}
    try:
        data = jalankan_pengembangan_smartphone()
        if request.method == "POST":
            try:
                list_asli = _parse_angka(request.POST.get("harga_asli", ""))
                list_diskon = _parse_angka(request.POST.get("harga_diskon", ""))
                data["numpy_diskon"] = hitung_diskon_numpy(list_asli, list_diskon)
            except ValueError as err:
                konteks["numpy_error"] = str(err)
        konteks["pengembangan_data"] = data
    except Exception as exc:
        konteks["pengembangan_error"] = str(exc)

    return render(request, "prediksi_app/index.html", konteks)


def api_prediksi(request):
    return JsonResponse({"status": "ok"})


def api_grafik(request):
    return JsonResponse({"status": "ok"})