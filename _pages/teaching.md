---
layout: default
title: Teaching
description: Notes from one-on-one tutoring, grouped by subject.
permalink: /teaching/
---

{% assign items = site.teaching %}

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
            <p>I write my own notes and problem sets for these sessions. Selected ones are collected below, with a home page for each subject (written in Korean).</p>
            <p>Tutoring inquiries: <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
        </div>
    </header>

    <section class="teaching-group">
        <h2 class="teaching-subject">Subjects</h2>
        <div class="teaching-hubs">
            {% for subject in site.data.teaching %}
            {% assign notes = items | where: "subject", subject.key | sort: "note" %}
            <article class="teaching-hub">
                <h3 class="teaching-hub-name">
                    <a href="{{ '/teaching/' | append: subject.slug | append: '/' | relative_url }}">{{ subject.name }}</a>
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
                <a href="{{ '/teaching/' | append: subject.slug | append: '/' | relative_url }}" class="read-more">{{ subject.name }} home ({{ notes.size }} notes) &rarr;</a>
            </article>
            {% endfor %}
        </div>
    </section>

    {% if items.size == 0 %}
    <p class="no-posts">No notes yet.</p>
    {% endif %}
</div>
