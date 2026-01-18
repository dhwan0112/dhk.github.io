---
layout: page
title: Research Results
description: Collection of experimental data, visualizations, and research outputs
permalink: /research-results/
---

<section class="results-gallery">
    <div class="container">
        <h2 class="section-title">Image Gallery</h2>
        <div class="gallery-grid">
            {% for image in site.data.research-results.images %}
            <div class="gallery-item">
                <div class="gallery-image">
                    {% if image.imageUrl %}
                    <img src="{{ image.imageUrl | relative_url }}" alt="{{ image.title }}">
                    {% else %}
                    <div class="placeholder-gallery">
                        <i class="fas fa-image"></i>
                        <p>Image Placeholder</p>
                    </div>
                    {% endif %}
                </div>
                <div class="gallery-info">
                    <h3>{{ image.title }}</h3>
                    <p>{{ image.description }}</p>
                    <span class="gallery-date">Date: {{ image.date }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<section class="video-gallery">
    <div class="container">
        <h2 class="section-title">Video Gallery</h2>
        <div class="video-grid">
            {% for video in site.data.research-results.videos %}
            <div class="video-item">
                <div class="video-wrapper">
                    {% if video.videoUrl %}
                        {% if video.videoType == 'youtube' %}
                        <iframe src="{{ video.videoUrl }}" frameborder="0" allowfullscreen></iframe>
                        {% else %}
                        <video controls>
                            <source src="{{ video.videoUrl | relative_url }}" type="video/mp4">
                        </video>
                        {% endif %}
                    {% else %}
                    <div class="placeholder-video">
                        <i class="fas fa-play-circle"></i>
                        <p>Video Placeholder</p>
                    </div>
                    {% endif %}
                </div>
                <div class="video-info">
                    <h3>{{ video.title }}</h3>
                    <p>{{ video.description }}</p>
                    <span class="video-date">Date: {{ video.date }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<section class="data-viz">
    <div class="container">
        <h2 class="section-title">Data Visualizations</h2>
        <p class="section-description">Interactive plots, graphs, and charts from computational and experimental data</p>
        <div class="viz-grid">
            {% for viz in site.data.research-results.visualizations %}
            <div class="viz-item">
                <div class="viz-preview">
                    {% if viz.imageUrl %}
                    <img src="{{ viz.imageUrl | relative_url }}" alt="{{ viz.title }}">
                    {% else %}
                    <div class="placeholder-viz">
                        <i class="fas fa-chart-line"></i>
                        <p>Graph Placeholder</p>
                    </div>
                    {% endif %}
                </div>
                <div class="viz-info">
                    <h3>{{ viz.title }}</h3>
                    <p>{{ viz.description }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
