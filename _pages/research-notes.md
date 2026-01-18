---
layout: page
title: Research Notes
description: Laboratory notebook and research journal documenting experiments, observations, and insights
permalink: /research-notes/
---

<section class="lab-notes">
    <div class="container">
        <div class="notes-container">
            {% assign sorted_notes = site.notes | sort: 'date' | reverse %}
            {% for note in sorted_notes %}
            <article class="note-entry">
                <div class="note-header">
                    <h2 class="note-title">
                        <a href="{{ note.url | relative_url }}">{{ note.title }}</a>
                    </h2>
                    <div class="note-meta">
                        <span class="note-date"><i class="far fa-calendar"></i> {{ note.date | date: "%Y-%m-%d" }}</span>
                        {% if note.category %}
                        <span class="note-category"><i class="fas fa-tag"></i> {{ note.category }}</span>
                        {% endif %}
                    </div>
                </div>
                <div class="note-content">
                    <p>{{ note.excerpt | strip_html | truncate: 200 }}</p>
                    <a href="{{ note.url | relative_url }}" class="read-more">Read more →</a>
                </div>
            </article>
            {% endfor %}

            {% if site.notes.size == 0 %}
            <p class="no-posts">No research notes yet. Check back soon!</p>
            {% endif %}
        </div>
    </div>
</section>
