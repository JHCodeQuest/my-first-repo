import sqlite3
from pathlib import Path

import frontmatter
import markdown
from flask import Flask, abort, g, redirect, render_template, url_for

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
DB_PATH = BASE_DIR / "progress.db"
TRACKS = {"aws": "AWS", "azure": "Azure"}

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.execute(
            "CREATE TABLE IF NOT EXISTS completed "
            "(track TEXT, slug TEXT, PRIMARY KEY (track, slug))"
        )
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def load_lessons(track):
    track_dir = CONTENT_DIR / track
    lessons = []
    for path in track_dir.glob("*.md"):
        post = frontmatter.load(path)
        lessons.append(
            {
                "slug": path.stem,
                "title": post.get("title", path.stem),
                "summary": post.get("summary", ""),
                "order": post.get("order", 0),
            }
        )
    lessons.sort(key=lambda lesson: lesson["order"])
    return lessons


def load_lesson(track, slug):
    path = CONTENT_DIR / track / f"{slug}.md"
    if not path.exists():
        abort(404)
    post = frontmatter.load(path)
    html = markdown.markdown(post.content, extensions=["fenced_code", "tables"])
    return {
        "title": post.get("title", slug),
        "summary": post.get("summary", ""),
        "html": html,
    }


def completed_slugs(track):
    db = get_db()
    rows = db.execute("SELECT slug FROM completed WHERE track = ?", (track,))
    return {row[0] for row in rows}


@app.route("/")
def dashboard():
    tracks = []
    for track_key, track_name in TRACKS.items():
        lessons = load_lessons(track_key)
        done = completed_slugs(track_key)
        tracks.append(
            {
                "key": track_key,
                "name": track_name,
                "total": len(lessons),
                "done": len(done),
            }
        )
    return render_template("dashboard.html", tracks=tracks)


@app.route("/track/<track>")
def track_view(track):
    if track not in TRACKS:
        abort(404)
    lessons = load_lessons(track)
    done = completed_slugs(track)
    for lesson in lessons:
        lesson["done"] = lesson["slug"] in done
    return render_template(
        "track.html", track_key=track, track_name=TRACKS[track], lessons=lessons
    )


@app.route("/track/<track>/<slug>")
def lesson_view(track, slug):
    if track not in TRACKS:
        abort(404)
    lesson = load_lesson(track, slug)
    done = slug in completed_slugs(track)
    return render_template(
        "lesson.html",
        track_key=track,
        track_name=TRACKS[track],
        slug=slug,
        lesson=lesson,
        done=done,
    )


@app.route("/track/<track>/<slug>/complete", methods=["POST"])
def mark_complete(track, slug):
    if track not in TRACKS:
        abort(404)
    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO completed (track, slug) VALUES (?, ?)", (track, slug)
    )
    db.commit()
    return redirect(url_for("lesson_view", track=track, slug=slug))


if __name__ == "__main__":
    app.run(debug=True)
