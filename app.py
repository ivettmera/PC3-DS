'''
Controlador Principal
'''
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, flash

import storage
from infraestructure.db import seed_demo_data
from infraestructure.notification import NotificationService
from infraestructure.crypto import CryptoService
from infraestructure.congress_client import CongressClient
from services.proposal import ProposalFacade
from services.signature import SignatureProxy
from services.resource import ResourceService

app = Flask(__name__)
app.secret_key = "voz-ciudadana-demo"

seed_demo_data()
_facade    = ProposalFacade(notification_service=NotificationService())
_sig_proxy       = SignatureProxy(
    crypto_service       = CryptoService(),
    notification_service = NotificationService(),
    congress_client      = CongressClient(),
)
_resource_service = ResourceService()


@app.route("/")
def index():
    proposals = list(storage.proposals.values())
    today     = date.today()
    return render_template("index.html", proposals=proposals, today=today)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        ok, error, proposal = _facade.create_and_publish(
            title         = request.form.get("title",         ""),
            motivation    = request.form.get("motivation",    ""),
            articles      = request.form.get("articles",      ""),
            category      = request.form.get("category",      "General"),
            collective_id = request.form.get("collective_id", "COL-001"),
        )
        if ok:
            flash(f"ILC '{proposal.title}' publicada correctamente.", "success")
            return redirect(url_for("index"))
        flash(error, "danger")

    collectives = [c for c in storage.collectives.values() if c.approved]
    return render_template("create.html", collectives=collectives)


@app.route("/detail/<proposal_id>")
def detail(proposal_id):
    proposal  = storage.proposals.get(proposal_id)
    if not proposal:
        flash("Iniciativa no encontrada.", "danger")
        return redirect(url_for("index"))
    sigs      = storage.signatures.get(proposal_id, [])
    resources = storage.resources.get(proposal_id, [])
    citizens  = list(storage.citizens.values())
    today     = date.today()
    return render_template(
        "details.html",
        proposal  = proposal,
        sig_count = len(sigs),
        resources = resources,
        citizens  = citizens,
        today     = today,
    )


@app.route("/sign/<proposal_id>", methods=["POST"])
def sign(proposal_id):
    citizen_id = request.form.get("citizen_id", "CIT-001")
    try:
        _sig_proxy.sign(citizen_id, proposal_id)
        flash("Firma registrada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("detail", proposal_id=proposal_id))


@app.route("/resource/<proposal_id>", methods=["POST"])
def resource(proposal_id):
    try:
        _resource_service.add(
            proposal_id = proposal_id,
            author_id   = request.form.get("citizen_id", "CIT-001"),
            tipo        = request.form.get("tipo",        "COMENTARIO"),
            content     = request.form.get("content",     ""),
        )
        flash("Recurso agregado correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("detail", proposal_id=proposal_id))

if __name__ == "__main__":
    app.run(debug=True)
