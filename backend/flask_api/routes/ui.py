"""
UI/Template Routes
"""

from flask import Blueprint, render_template

ui_bp = Blueprint('ui', __name__)


@ui_bp.route("/")
def landing():
    """Serve the landing page"""
    return render_template("index.html")


@ui_bp.route("/workspace")
def workspace():
    """Serve the workspace UI"""
    return render_template("app.html")


@ui_bp.route("/projects")
def k2_projects():
    """Placeholder route for K2 Projects hub"""
    return render_template("k2_projects/index.html")


@ui_bp.route("/search/engines")
def k2_search():
    """Placeholder route for the K2 search engine hub"""
    return render_template("k2_search/index.html")
