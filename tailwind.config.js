/** @type {import('tailwindcss').Config} */
module.exports = {
  // Adjust content paths to match your project
  content: ["./**/*.html"],
  theme: {
    extend: {

      /* ----------------------------------------------------------------
         Colors — mapped to CSS custom properties from design-tokens.css
         ---------------------------------------------------------------- */
      colors: {
        // Brand greens
        brand: {
          50:  "var(--green-50)",   // #00ffc4
          100: "var(--green-100)",  // #00e6b0
          200: "var(--green-200)",  // #00b389
          300: "var(--green-300)",  // #008066
        },
        // Semantic surface colors
        surface: {
          DEFAULT: "var(--color-surface-1)",
          1:      "var(--color-surface-1)",
          2:      "var(--color-surface-2)",
          hover:  "var(--color-surface-hover)",
        },
        // Semantic accent
        primary: {
          DEFAULT: "var(--color-primary)",
          light:   "var(--color-primary-light)",
          bright:  "var(--color-primary-bright)",
          dark:    "var(--color-primary-dark)",
        },
        // Background
        bg: "var(--color-bg)",
      },

      /* ----------------------------------------------------------------
         Text Color — semantic text tokens
         ---------------------------------------------------------------- */
      textColor: {
        primary:   "var(--text-primary)",
        secondary: "var(--text-secondary)",
        tertiary:  "var(--text-tertiary)",
        muted:     "var(--text-muted)",
        accent:    "var(--text-accent)",
      },

      /* ----------------------------------------------------------------
         Typography
         ---------------------------------------------------------------- */
      fontFamily: {
        display: ["Playfair Display", "serif"],
        body:    ["Inter", "sans-serif"],
      },
      fontSize: {
        xxs: ["0.625rem", { lineHeight: "1" }],         // 10px micro labels
        xs:  ["0.75rem",  { lineHeight: "1.2" }],       // 12px labels
        sm:  ["0.875rem", { lineHeight: "1.4" }],       // 14px
        base:["1rem",     { lineHeight: "1.5" }],       // 16px
        lg:  ["1.125rem", { lineHeight: "1.625" }],     // 18px body
        xl:  ["1.25rem",  { lineHeight: "1.5" }],       // 20px
        "2xl":["1.5rem",  { lineHeight: "1.3" }],       // 24px
        "4xl":["2.25rem", { lineHeight: "1.1" }],       // 36px heading mobile
        "6xl":["3.75rem", { lineHeight: "1.1" }],       // 60px heading desktop
      },
      lineHeight: {
        tight:   "1.1",
        snug:    "1.3",
        normal:  "1.5",
        relaxed: "1.625",
      },

      /* ----------------------------------------------------------------
         Spacing
         ---------------------------------------------------------------- */
      spacing: {
        "section-compact":  "var(--section-py-compact)",   // 4rem
        "section-standard": "var(--section-py-standard)",  // 6rem
        "section-hero":     "var(--section-py-hero)",      // 8rem
        "content-px":       "var(--content-px)",           // 1.5rem
      },

      /* ----------------------------------------------------------------
         Max Width
         ---------------------------------------------------------------- */
      maxWidth: {
        container: "var(--container-max)", // 1152px
      },

      /* ----------------------------------------------------------------
         Border Radius
         ---------------------------------------------------------------- */
      borderRadius: {
        lg:       "var(--radius-lg)",
        xl:       "var(--radius-xl)",
        "2xl":    "var(--radius-2xl)",
        "3xl":    "var(--radius-3xl)",
        full:     "var(--radius-full)",
        card:     "var(--radius-card)",
        "card-lg":"var(--radius-card-lg)",
        "card-inner": "var(--radius-card-inner)",
        button:   "var(--radius-button)",
        pill:     "var(--radius-pill)",
      },

      /* ----------------------------------------------------------------
         Box Shadow
         ---------------------------------------------------------------- */
      boxShadow: {
        sm:       "var(--shadow-sm)",
        md:       "var(--shadow-md)",
        lg:       "var(--shadow-lg)",
        "2xl":    "var(--shadow-2xl)",
        card:     "var(--shadow-card)",
        elevated: "var(--shadow-elevated)",
        glow:     "var(--shadow-glow)",
        "glow-sm":"var(--glow-sm)",
        "glow-md":"var(--glow-md)",
        "glow-lg":"var(--glow-lg)",
        "glow-xl":"var(--glow-xl)",
      },

      /* ----------------------------------------------------------------
         Z-Index
         ---------------------------------------------------------------- */
      zIndex: {
        base:      "var(--z-base)",       // 0
        content:   "var(--z-content)",     // 10
        sticky:    "var(--z-sticky)",      // 20
        "sticky-hi":"var(--z-sticky-hi)",  // 35
        nav:       "var(--z-nav)",         // 40
        modal:     "var(--z-modal)",       // 100
        skip:      "var(--z-skip)",        // 200
      },

      /* ----------------------------------------------------------------
         Background Image (gradients)
         ---------------------------------------------------------------- */
      backgroundImage: {
        "cta-gradient": "var(--cta-gradient)",
      },

      /* ----------------------------------------------------------------
         Border Color
         ---------------------------------------------------------------- */
      borderColor: {
        DEFAULT:  "var(--border-default)",
        subtle:   "var(--border-subtle)",
        accent:   "var(--border-accent)",
      },

    },
  },
  plugins: [],
};
