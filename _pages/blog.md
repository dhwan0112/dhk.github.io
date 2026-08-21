---
layout: default
title: Blog
description: Notes on computational chemistry — ORCA, LAMMPS, Quantum ESPRESSO, and the scripting around them.
permalink: /blog/
---

{% assign tag_names = "" | split: "" %}
{% for t in site.tags %}{% assign tag_names = tag_names | push: t[0] %}{% endfor %}
{% assign tag_names = tag_names | sort_natural %}

<div class="blog-index">
    <header class="blog-index-header">
        <h1 class="blog-index-title">Blog</h1>
        <p class="blog-index-lede">{{ page.description }}</p>
        {% if tag_names.size > 0 %}
        <nav class="blog-tag-nav" aria-label="Filter by tag">
            <a href="{{ '/blog/' | relative_url }}" class="blog-tag-link is-active" data-tag="">All</a>
            {% for name in tag_names %}
            <a href="{{ '/blog/' | relative_url }}?tag={{ name | uri_escape }}" class="blog-tag-link" data-tag="{{ name }}">{{ name }}</a>
            {% endfor %}
        </nav>
        {% endif %}
    </header>

    <div class="post-list" id="post-list">
        {% for post in site.posts %}
        <article class="post-item" data-tags="{{ post.tags | join: '|' }}">
            <h2 class="post-item-title">
                <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
            </h2>
            <p class="post-item-excerpt">{% if post.description %}{{ post.description }}{% else %}{{ post.content | strip_html | normalize_whitespace | truncate: 320 }}{% endif %}</p>
            <a href="{{ post.url | relative_url }}" class="read-more">Read more</a>
            <footer class="post-item-foot">
                <div class="post-item-tags">
                    {% for tag in post.tags %}
                    <a href="{{ '/blog/' | relative_url }}?tag={{ tag | uri_escape }}" class="tag" data-tag="{{ tag }}">{{ tag }}</a>
                    {% endfor %}
                </div>
                <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %-d, %Y" }}</time>
            </footer>
        </article>
        {% endfor %}

        {% if site.posts.size == 0 %}
        <p class="no-posts">No posts yet.</p>
        {% endif %}
        <p class="no-posts" id="post-list-empty" hidden>No posts with this tag.</p>
    </div>
</div>
