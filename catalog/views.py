from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Plant, PlantCategory

PER_PAGE = 24


def plant_list(request):
    """Browse the whole catalogue with search and filtering."""
    plants = Plant.objects.select_related("category")

    category_slug = (request.GET.get("category") or "").strip()
    query = (request.GET.get("q") or "").strip()
    pet_safe = request.GET.get("pet_safe") == "on"

    if category_slug:
        plants = plants.filter(category__slug=category_slug)
    if query:
        plants = plants.filter(
            Q(name__icontains=query) | Q(scientific_name__icontains=query)
        )
    if pet_safe:
        plants = plants.filter(toxicity=False)

    total = plants.count()
    page_obj = Paginator(plants, PER_PAGE).get_page(request.GET.get("page"))

    # Preserve the active filters in pagination links.
    params = request.GET.copy()
    params.pop("page", None)

    context = {
        "page_obj": page_obj,
        "categories": PlantCategory.objects.all(),
        "active_category": category_slug,
        "query": query,
        "pet_safe": pet_safe,
        "total": total,
        "querystring": params.urlencode(),
    }
    return render(request, "catalog/plant_list.html", context)


def plant_detail(request, pk):
    """Full information for a single plant."""
    plant = get_object_or_404(Plant.objects.select_related("category"), pk=pk)
    return render(request, "catalog/plant_detail.html", {"plant": plant})
