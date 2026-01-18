---
layout: page
title: Blog
description: Thoughts, tutorials, and notes on computational chemistry, programming, and more
permalink: /blog/
---

<section class="blog-list">
    <div class="container">
        <div class="posts-container">
            {% for post in site.posts %}
            <article class="post-preview">
                <div class="post-header">
                    <h2 class="post-title">
                        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                    </h2>
                    <div class="post-meta">
                        <span class="post-date"><i class="far fa-calendar"></i> {{ post.date | date: "%Y-%m-%d" }}</span>
                        {% if post.category %}
                        <span class="post-category"><i class="fas fa-tag"></i> {{ post.category }}</span>
                        {% endif %}
                    </div>
                </div>
                <div class="post-excerpt">
                    <p>{{ post.excerpt | strip_html | truncate: 250 }}</p>
                    <a href="{{ post.url | relative_url }}" class="read-more">Read more →</a>
                </div>
                {% if post.tags %}
                <div class="post-tags">
                    {% for tag in post.tags %}
                    <span class="tag">{{ tag }}</span>
                    {% endfor %}
                </div>
                {% endif %}
            </article>
            {% endfor %}

            {% if site.posts.size == 0 %}
            <p class="no-posts">No posts yet. Check back soon!</p>
            {% endif %}
        </div>
    </div>
</section>
