from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FILE = 'video_ideas.json'

# Load video ideas from JSON file
def load_video_ideas():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save video ideas to JSON file
def save_video_ideas(ideas):
    with open(DATA_FILE, 'w') as file:
        json.dump(ideas, file, indent=4)

@app.route('/')
def index():
    video_ideas = load_video_ideas()
    return render_template('index.html', video_ideas=video_ideas)

@app.route('/add', methods=['POST'])
def add_idea():
    idea = request.form.get('idea')
    script = request.form.get('script')
    
    if not idea or not script:
        flash('Both fields are required!')
        return redirect(url_for('index'))

    video_ideas = load_video_ideas()
    video_ideas[idea] = {'script': script, 'favorite': False, 'archived': False}
    save_video_ideas(video_ideas)
    flash('Video idea added successfully!')
    return redirect(url_for('index'))

@app.route('/edit/<idea>', methods=['GET', 'POST'])
def edit_idea(idea):
    video_ideas = load_video_ideas()
    if request.method == 'POST':
        script = request.form.get('script')
        video_ideas[idea]['script'] = script
        save_video_ideas(video_ideas)
        flash('Video idea updated successfully!')
        return redirect(url_for('index'))
    
    return render_template('edit.html', idea=idea, script=video_ideas[idea]['script'])

@app.route('/delete/<idea>', methods=['POST'])
def delete_idea(idea):
    video_ideas = load_video_ideas()
    if idea in video_ideas:
        del video_ideas[idea]
        save_video_ideas(video_ideas)
        flash('Video idea deleted successfully!')
    return redirect(url_for('index'))

@app.route('/favorite/<idea>', methods=['POST'])
def favorite_idea(idea):
    video_ideas = load_video_ideas()
    if idea in video_ideas:
        video_ideas[idea]['favorite'] = not video_ideas[idea]['favorite']
        save_video_ideas(video_ideas)
        flash('Video idea updated successfully!')
    return redirect(url_for('index'))

@app.route('/archive/<idea>', methods=['POST'])
def archive_idea(idea):
    video_ideas = load_video_ideas()
    if idea in video_ideas:
        video_ideas[idea]['archived'] = not video_ideas[idea]['archived']
        save_video_ideas(video_ideas)
        flash('Video idea updated successfully!')
    return redirect(url_for('index'))

@app.route('/favorites')
def favorites():
    video_ideas = load_video_ideas()
    favorite_ideas = {idea: data for idea, data in video_ideas.items() if data['favorite']}
    return render_template('favorites.html', video_ideas=favorite_ideas)

@app.route('/archive')
def archive():
    video_ideas = load_video_ideas()
    archived_ideas = {idea: data for idea, data in video_ideas.items() if data['archived']}
    return render_template('archive.html', video_ideas=archived_ideas)

if __name__ == '__main__':
    app.run(debug=True)
