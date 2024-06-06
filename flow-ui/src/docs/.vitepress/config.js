// docs/.vitepress/config.js
module.exports = {
    title: 'My Project Documentation',
    description: 'A VitePress site for my existing project',
    themeConfig: {
      nav: [
        { text: 'Guide', link: '/guide/getting-started' },
      ],
      sidebar: {
        '/guide/': [
          {
            text: 'Guide',
            children: [
              { text: 'Fast API', link: '/guide/fast-api' },
            ]
          }
        ]
      }
    }
};
