// knowledge-graph.js
(function() {
  // Check for D3.js
  if (typeof d3 === 'undefined') {
    var script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js';
    script.onload = renderGraph;
    document.head.appendChild(script);
  } else {
    renderGraph();
  }

  function renderGraph() {
    const data = JSON.parse(document.getElementById('posts-graph-data').textContent);
    if (!data || !Array.isArray(data) || data.length === 0) {
      document.getElementById('knowledge-graph-container').innerHTML = '<p class="text-muted">No posts yet. Be the first to start the discussion!</p>';
      return;
    }

    // Build nodes and links
    const nodes = [];
    const links = [];
    const nodeMap = {};

    data.forEach(postData => {
      const post = postData.post;
      const node = {
        id: post.pk,
        title: post.title,
        url: `/${post.rabble_id}/!${post.subrabble_id}/${post.pk}/`,
        author: post.anonymous ? 'anonymous' : (post.user_id && post.user_id.username ? post.user_id.username : 'unknown'),
        likes: post.post_likes ? post.post_likes.length : 0,
        comments: post.comment_set ? post.comment_set.length : 0
      };
      nodes.push(node);
      nodeMap[post.pk] = node;
    });

    data.forEach(postData => {
      const post = postData.post;
      postData.outgoing.forEach(rel => {
        links.push({
          source: post.pk,
          target: rel.target_post_id,
          type: rel.relationship_type
        });
      });
    });

    // D3.js force-directed graph
    const width = document.getElementById('knowledge-graph-container').offsetWidth;
    const height = 600;
    const colorMap = {
      'contradicts': '#dc3545',
      'supports': '#198754',
      'elaborates': '#0dcaf0',
      'questions': '#ffc107',
      'shifts_focus': '#6c757d',
      'default': '#adb5bd'
    };

    // Clear previous SVG
    document.getElementById('knowledge-graph-container').innerHTML = '';
    const svg = d3.select('#knowledge-graph-container')
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    // Tooltip
    const tooltip = d3.select('body').append('div')
      .attr('class', 'graph-tooltip')
      .style('position', 'absolute')
      .style('z-index', '10')
      .style('visibility', 'hidden')
      .style('background', '#fff')
      .style('border', '1px solid #ccc')
      .style('padding', '8px')
      .style('border-radius', '6px')
      .style('font-size', '0.95rem');

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(250))
      .force('charge', d3.forceManyBody().strength(-800))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collide', d3.forceCollide(80));

    // Draw links
    const link = svg.append('g')
      .attr('stroke', '#aaa')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', 2)
      .attr('stroke', d => colorMap[d.type] || colorMap['default']);

    // Draw link labels (relationship types)
    const linkLabel = svg.append('g')
      .selectAll('text.link-label')
      .data(links)
      .join('text')
      .attr('class', 'link-label')
      .attr('text-anchor', 'middle')
      .attr('font-size', '0.85rem')
      .attr('fill', d => colorMap[d.type] || colorMap['default'])
      .attr('pointer-events', 'none')
      .attr('opacity', 0.95)
      .style('font-weight', 'bold')
      .text(d => d.type);

    // Draw nodes
    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 28)
      .attr('fill', '#0d6efd')
      .attr('cursor', 'pointer')
      .on('mouseover', function(event, d) {
        tooltip.html(`<strong>${d.title}</strong><br>By: ${d.author}<br>👍 ${d.likes} | 💬 ${d.comments}`)
          .style('visibility', 'visible');
        d3.select(this).attr('fill', '#6610f2');
      })
      .on('mousemove', function(event) {
        tooltip.style('top', (event.pageY + 15) + 'px')
               .style('left', (event.pageX + 15) + 'px');
      })
      .on('mouseout', function() {
        tooltip.style('visibility', 'hidden');
        d3.select(this).attr('fill', '#0d6efd');
      })
      .on('click', function(event, d) {
        window.location.href = d.url;
      });

    // Node labels
    const label = svg.append('g')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .attr('text-anchor', 'middle')
      .attr('dy', 4)
      .attr('pointer-events', 'none')
      .style('font-size', '0.95rem')
      .style('font-weight', 'bold')
      .text(d => d.title.length > 18 ? d.title.slice(0, 15) + '…' : d.title);

    const padding = 40; // Minimum distance from edge

    function clamp(val, min, max) {
      return Math.max(min, Math.min(max, val));
    }

    simulation.on('tick', () => {
      link
        .attr('x1', d => clamp(d.source.x, padding, width - padding))
        .attr('y1', d => clamp(d.source.y, padding, height - padding))
        .attr('x2', d => clamp(d.target.x, padding, width - padding))
        .attr('y2', d => clamp(d.target.y, padding, height - padding));

      // Relationship labels: parallel to the link, always upright
      linkLabel
        .attr('x', d => (clamp(d.source.x, padding, width - padding) + clamp(d.target.x, padding, width - padding)) / 2)
        .attr('y', d => (clamp(d.source.y, padding, height - padding) + clamp(d.target.y, padding, height - padding)) / 2)
        .attr('transform', d => {
          const x1 = clamp(d.source.x, padding, width - padding);
          const x2 = clamp(d.target.x, padding, width - padding);
          const y1 = clamp(d.source.y, padding, height - padding);
          const y2 = clamp(d.target.y, padding, height - padding);
          const mx = (x1 + x2) / 2;
          const my = (y1 + y2) / 2;
          let angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
          if (angle > 90 || angle < -90) {
            angle += 180;
          }
          return `rotate(${angle}, ${mx}, ${my})`;
        })
        .attr('dy', '-0.4em');

      node
        .attr('cx', d => d.x = clamp(d.x, padding, width - padding))
        .attr('cy', d => d.y = clamp(d.y, padding, height - padding));

      // Standardize node label positioning
      const nodeRadius = 28;
      const labelOffset = 8; // Distance from node circle edge
      const totalOffset = nodeRadius + labelOffset;

      label.each(function(d) {
        const connectedLinks = links.filter(l => l.source === d || l.target === d);
        let vector = { x: 0, y: 0 };
        
        if (connectedLinks.length > 0) {
            connectedLinks.forEach(l => {
                const otherNode = l.source === d ? l.target : l.source;
                vector.x += otherNode.x - d.x;
                vector.y += otherNode.y - d.y;
            });

            const len = Math.sqrt(vector.x * vector.x + vector.y * vector.y);
            if (len > 0) {
                vector.x /= len;
                vector.y /= len;
            } else {
                vector.x = 0;
                vector.y = -1; // Default to above if vectors cancel out
            }
        } else {
            vector.x = 0;
            vector.y = -1; // Default to above for isolated nodes
        }

        const labelX = d.x - vector.x * totalOffset;
        const labelY = d.y - vector.y * totalOffset;
        
        let textAnchor = "middle";
        if (vector.x > 0.5) textAnchor = "end";
        else if (vector.x < -0.5) textAnchor = "start";

        let dominantBaseline = "middle";
        if (vector.y > 0.5) dominantBaseline = "auto";
        else if (vector.y < -0.5) dominantBaseline = "hanging";
        
        d3.select(this)
          .attr('x', clamp(labelX, padding, width - padding))
          .attr('y', clamp(labelY, padding, height-padding))
          .attr('text-anchor', textAnchor)
          .attr('dominant-baseline', dominantBaseline);
      });
    });
  }
})(); 