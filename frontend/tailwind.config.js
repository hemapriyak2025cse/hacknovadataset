/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        // ── Core brand ──────────────────────────────────────
        accent: {
          DEFAULT:  '#E8440A',   // strong orange-red
          hover:    '#D13A08',
          light:    '#FDF1EC',
          muted:    '#F4A07A',
        },
        teal: {
          DEFAULT:  '#0D9488',
          light:    '#CCFBF1',
          dark:     '#0F766E',
        },
        // ── Surfaces ────────────────────────────────────────
        canvas:   '#F5F2EE',     // warm off-white / cream
        card:     '#FDFCFB',     // slightly warmer white
        'card-dark': '#1C1917',  // near-black card
        // ── Charcoal scale ──────────────────────────────────
        charcoal: {
          950: '#0C0A09',
          900: '#1C1917',
          800: '#292524',
          700: '#44403C',
          600: '#57534E',
          500: '#78716C',
          400: '#A8A29E',
          300: '#D6D3D1',
          200: '#E7E5E4',
          100: '#F5F5F4',
          50:  '#FAFAF9',
        },
        // ── Risk ────────────────────────────────────────────
        risk: {
          low:          '#16A34A',
          'low-bg':     '#F0FDF4',
          medium:       '#D97706',
          'medium-bg':  '#FFFBEB',
          high:         '#DC2626',
          'high-bg':    '#FEF2F2',
          critical:     '#991B1B',
          'critical-bg':'#FFF1F2',
        },
        // ── Legacy aliases (keep WhatShouldWeDo working) ────
        brand: {
          orange:        '#E8440A',
          'orange-light':'#FDF1EC',
          'orange-dark': '#D13A08',
          teal:          '#0D9488',
          'teal-light':  '#CCFBF1',
          'teal-dark':   '#0F766E',
        },
        surface: {
          DEFAULT: '#F5F2EE',
          card:    '#FDFCFB',
          low:     '#F0EDE9',
          high:    '#E7E5E4',
        },
        ink: {
          DEFAULT: '#1C1917',
          muted:   '#78716C',
          subtle:  '#A8A29E',
        },
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        '2xs': ['10px', { lineHeight: '14px' }],
      },
      boxShadow: {
        card:     '0 1px 2px 0 rgba(28,25,23,0.04)',
        elevated: '0 4px 24px 0 rgba(28,25,23,0.08)',
        'inner-sm': 'inset 0 1px 2px rgba(28,25,23,0.06)',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      animation: {
        beacon:    'beacon 2s ease-in-out infinite',
        'fade-in': 'fadeIn 0.25s ease-out',
        'slide-up':'slideUp 0.25s ease-out',
      },
      keyframes: {
        beacon:   { '0%,100%': { opacity: 1 }, '50%': { opacity: 0.35 } },
        fadeIn:   { from: { opacity: 0 }, to: { opacity: 1 } },
        slideUp:  { from: { opacity: 0, transform: 'translateY(6px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
}
