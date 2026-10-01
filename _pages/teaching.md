---
layout: default
title: Teaching
description: Notes from one-on-one tutoring, grouped by subject.
permalink: /teaching/
---

{% assign items = site.teaching | sort: "order" %}
{% assign subjects = items | map: "subject" | uniq %}

<div class="blog-index">
    <header class="blog-index-header">
        <h1 class="blog-index-title">Teaching</h1>
        <div class="teaching-summary">
            <p>I started tutoring in Grade 11 (around 2020) and still teach, one-on-one and online.</p>
            <ul>
                <li><strong>AP:</strong> Chemistry, Physics, Biology, Calculus, Statistics, mostly for international-school students</li>
                <li><strong>School science and mathematics:</strong> middle and high school courses outside the AP track</li>
                <li><strong>Competition mathematics:</strong> AMC preparation</li>
            </ul>
            <p>I write my own notes and problem sets for these sessions. Selected ones are below, grouped by subject (written in Korean).</p>
            <p>Tutoring inquiries: <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
        </div>
    </header>

    {% for subject in subjects %}
    <section class="teaching-group">
        <h2 class="teaching-subject">{{ subject }}</h2>
        <div class="post-list">
            {% for item in items %}{% if item.subject == subject %}
            <article class="post-item">
                <h3 class="post-item-title">
                    <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
                </h3>
                <p class="post-item-excerpt">{{ item.description }}</p>
                <a href="{{ item.url | relative_url }}" class="read-more">Read more</a>
                <footer class="post-item-foot">
                    <div class="post-item-tags">
                        {% for tag in item.tags %}<span class="tag">{{ tag }}</span>{% endfor %}
                    </div>
                    <time datetime="{{ item.date | date_to_xmlschema }}">{{ item.date | date: "%b %-d, %Y" }}</time>
                </footer>
            </article>
            {% endif %}{% endfor %}
        </div>
    </section>
    {% endfor %}

    {% if items.size == 0 %}
    <p class="no-posts">No notes yet.</p>
    {% endif %}
</div>
