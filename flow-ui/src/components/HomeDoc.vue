<template>
  <section>
    <div class="w-[100%] text-center py-24 lg:py-56">
      <h1
        class="mb-4 text-4xl font-extrabold tracking-tight leading-none dark:text-white md:text-5xl lg:text-6xl"
      >
        Start building
      </h1>

      <div
        class="flex flex-col space-y-4 sm:flex-row sm:justify-center sm:space-y-0"
      >
        <a
          href="guide/ussd-intro"
          class="inline-flex justify-center items-center py-3 px-5 text-base font-medium text-center text-white rounded-lg bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900"
        >
          Get started
          <svg
            class="w-3.5 h-3.5 ms-2 rtl:rotate-180"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 14 10"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M1 5h12m0 0L9 1m4 4L9 9"
            />
          </svg>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts"></script>

<style scoped>
@tailwind base;
@tailwind components;
@tailwind utilities;
</style>
