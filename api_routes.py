from main import ICONS_DATABASE, app
from py_utils.common_utils.file_utils import sanitize_file_name
from py_utils.flask_utils.jsonify_utils import success_response, error_response
from flask import send_file, request, render_template
import os


@app.route('/')
@app.route('/explorer')
def route_explorer():
    return render_template('explorer.html')


@app.route('/search/<path:query>', methods=['GET'])
def route_search_icon(query: str):
    # Get style from query parameters
    style = request.args.get('style')

    if not query:
        return error_response(message='please enter query')

    query = query.lower()
    matched_icons = []
    exact_matches = []

    # Search through all icons for matches
    for key, icons in ICONS_DATABASE.items():
        # Check if query exactly matches the key
        if query == key.lower():
            exact_matches.extend(icons)
        # Check if query is a substring of the key
        elif query in key.lower():
            matched_icons.extend(icons)

    # Combine results with exact matches first
    all_icons = exact_matches + matched_icons

    if not all_icons:
        return error_response(message=f'Icons Not Found for {query}')

    # Filter by style if provided
    if style:
        filtered_icons = []
        for icon in all_icons:
            if style.lower() in [v.lower() for v in icon.get('varients', [])]:
                filtered_icons.append(icon)

        if not filtered_icons:
            return error_response(message=f'Icons Not Found for query: {query} & style: {style}')
        return success_response(data=filtered_icons)

    return success_response(data=all_icons)


@app.route('/icon/<path:icon>', methods=['GET'])
def route_view_icon(icon: str):
    # Get style from query parameters, default to 'baseline' if not provided
    style = request.args.get('style', 'baseline')

    # Construct the path based on whether style is provided
    path = f'svg/{sanitize_file_name(icon)}/{sanitize_file_name(style)}.svg'
    if not os.path.exists(path):
        return error_response(message=f'Icon not found: {icon}')

    response = send_file(
        path,
        mimetype='image/svg+xml',
        as_attachment=False
    )
    # Set longer cache duration for static SVG files (1 day)
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response
