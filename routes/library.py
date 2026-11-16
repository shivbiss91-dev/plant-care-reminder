from flask import Blueprint, render_template, request
from models import PlantLibrary

library_bp = Blueprint('library', __name__, url_prefix='/library')

@library_bp.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    query = PlantLibrary.query

    if search_query:
        query = query.filter(
            (PlantLibrary.name.ilike(f'%{search_query}%')) |
            (PlantLibrary.scientific_name.ilike(f'%{search_query}%')) |
            (PlantLibrary.description.ilike(f'%{search_query}%'))
        )

    if category_filter and category_filter != 'All':
        query = query.filter_by(category=category_filter)

    plants = query.order_by(PlantLibrary.name.asc()).all()
    categories = ['All', 'Indoor', 'Outdoor', 'Succulent', 'Flowering', 'Herb']

    return render_template(
        'library/index.html',
        plants=plants,
        search_query=search_query,
        selected_category=category_filter or 'All',
        categories=categories
    )

@library_bp.route('/<int:library_id>')
def detail(library_id):
    plant = PlantLibrary.query.get_or_404(library_id)
    return render_template('library/detail.html', plant=plant)
