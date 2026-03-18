<template>
  <div
    v-if="subrabbles.length"
    id="subrabblesCarousel"
    class="carousel slide"
    data-bs-ride="carousel"
  >
    <div class="carousel-indicators">
      <button
        v-for="(sr, i) in subrabbles"
        :key="'ind-' + sr.subrabble_community_id"
        type="button"
        data-bs-target="#subrabblesCarousel"
        :data-bs-slide-to="i"
        :class="{ active: i === 0 }"
        :aria-current="i === 0 ? 'true' : undefined"
        :aria-label="'SubRabble ' + (i + 1)"
      ></button>
    </div>

    <div class="carousel-inner">
      <div
        v-for="(sr, i) in subrabbles"
        :key="sr.subrabble_community_id"
        class="carousel-item"
        :class="{ active: i === 0 }"
      >
        <a
          :href="sr.url"
          class="subrabble-slide"
          :class="{ private: sr.private }"
        >
          <div class="slide-content">
            <div class="slide-header">
              <span v-if="sr.private" class="private-badge" title="Private SubRabble">
                <i class="bi bi-lock-fill"></i>
              </span>
            </div>
            <div class="slide-body">
              <h3 class="slide-title">!{{ sr.subrabble_community_id }}</h3>
              <h4 class="slide-subtitle">{{ sr.subrabble_name }}</h4>
              <p class="slide-description">{{ sr.description }}</p>
            </div>
            <div class="slide-footer">
              <span class="slide-action">
                Explore <i class="bi bi-arrow-right"></i>
              </span>
            </div>
          </div>
        </a>
      </div>
    </div>

    <button
      class="carousel-control-prev"
      type="button"
      data-bs-target="#subrabblesCarousel"
      data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
      class="carousel-control-next"
      type="button"
      data-bs-target="#subrabblesCarousel"
      data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>

  <div v-else class="no-subrabbles">
    <div class="empty-state">
      <i class="bi bi-collection"></i>
      <h3>No Rabbles Yet</h3>
      <p>Create one to get started!</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  subrabbles: { type: Array, default: () => [] },
})
</script>
