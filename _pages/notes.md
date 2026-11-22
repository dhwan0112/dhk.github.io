---
layout: default
title: Notes
description: Concept notes on mathematics and science, written in Korean and grouped by subject.
permalink: /notes/
---

{% assign items = site.notes %}

<div class="blog-index">
    <header class="blog-index-header">
        <h1 class="blog-index-title">Notes</h1>
        <p class="blog-index-lede">Concept notes on mathematics and science, written in Korean and grouped by subject.</p>
    </header>

    <section class="teaching-group">
        <h2 class="teaching-subject">Subjects</h2>
        <div class="teaching-hubs">
            {% for subject in site.data.notes %}
            {% assign notes = items | where: "subject", subject.key | sort: "note" %}
            <article class="teaching-hub">
                <h3 class="teaching-hub-name">
                    <a href="{{ '/notes/' | append: subject.slug | append: '/' | relative_url }}">{{ subject.name }}</a>
                    <span class="teaching-title-ko">{{ subject.ko }}</span>
                </h3>
                <p class="teaching-hub-lede">{{ subject.lede }}</p>
                <p class="teaching-hub-chapters">
                    {% for ch in subject.chapters %}{% for topic in ch.topics %}<span class="tag">{{ topic.name }}</span>{% endfor %}{% endfor %}
                </p>
                <ul class="teaching-hub-notes">
                    {% for item in notes %}
                    <li><a href="{{ item.url | relative_url }}"><span class="teaching-code">{{ item.note }}</span> {{ item.title }}</a></li>
                    {% endfor %}
                </ul>
                <a href="{{ '/notes/' | append: subject.slug | append: '/' | relative_url }}" class="read-more">All {{ subject.name }} notes ({{ notes.size }})</a>
            </article>
            {% endfor %}
        </div>
    </section>

    {% if items.size == 0 %}
    <p class="no-posts">No notes yet.</p>
    {% endif %}
</div>
