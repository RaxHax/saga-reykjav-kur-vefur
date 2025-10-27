/**
 * Configurable Icon Placeholders
 *
 * These are minimalist geometric icons that can be easily swapped.
 * Each icon is designed to be simple, modern, and tech-focused.
 *
 * To customize: Simply replace the SVG paths or import your own icon library.
 */

// Search Icon - Magnifying glass with AI sparkle
export const SearchIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle
      cx="20"
      cy="20"
      r="10"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
    />
    <path
      d="M27 27L38 38"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
    />
    {/* AI Sparkle */}
    <path
      d="M34 10L36 14L40 16L36 18L34 22L32 18L28 16L32 14L34 10Z"
      fill="currentColor"
      opacity="0.7"
    />
  </svg>
)

// Projects Icon - Three stacked layers
export const ProjectsIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect
      x="8"
      y="8"
      width="32"
      height="8"
      rx="2"
      stroke="currentColor"
      strokeWidth="2.5"
      fill="currentColor"
      opacity="0.3"
    />
    <rect
      x="8"
      y="20"
      width="32"
      height="8"
      rx="2"
      stroke="currentColor"
      strokeWidth="2.5"
      fill="currentColor"
      opacity="0.5"
    />
    <rect
      x="8"
      y="32"
      width="32"
      height="8"
      rx="2"
      stroke="currentColor"
      strokeWidth="2.5"
      fill="currentColor"
      opacity="0.7"
    />
  </svg>
)

// Archive Icon - Folder with document
export const ArchiveIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M8 12L16 6H32L40 12V38C40 39.1046 39.1046 40 38 40H10C8.89543 40 8 39.1046 8 38V12Z"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinejoin="round"
    />
    <path
      d="M16 20H32M16 26H28"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
)

// Index Icon - Database with layers
export const IndexIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <ellipse
      cx="24"
      cy="14"
      rx="12"
      ry="6"
      stroke="currentColor"
      strokeWidth="2.5"
    />
    <path
      d="M12 14V24C12 26.21 17.37 28 24 28C30.63 28 36 26.21 36 24V14"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
    />
    <path
      d="M12 24V34C12 36.21 17.37 38 24 38C30.63 38 36 36.21 36 34V24"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
    />
  </svg>
)

// Analytics Icon - Bar chart with trend arrow
export const AnalyticsIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="8" y="28" width="6" height="12" rx="1" fill="currentColor" opacity="0.5" />
    <rect x="18" y="20" width="6" height="20" rx="1" fill="currentColor" opacity="0.6" />
    <rect x="28" y="14" width="6" height="26" rx="1" fill="currentColor" opacity="0.8" />
    <path
      d="M34 12L40 6M40 6L40 12M40 6L34 12"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

// Settings Icon - Gear
export const SettingsIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle
      cx="24"
      cy="24"
      r="6"
      stroke="currentColor"
      strokeWidth="2.5"
    />
    <path
      d="M24 8V12M24 36V40M40 24H36M12 24H8M35.8 35.8L33 33M15 15L12.2 12.2M35.8 12.2L33 15M15 33L12.2 35.8"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
    />
  </svg>
)

// Vector Icon - Neural network nodes
export const VectorIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="4" fill="currentColor" opacity="0.8" />
    <circle cx="36" cy="12" r="4" fill="currentColor" opacity="0.8" />
    <circle cx="12" cy="36" r="4" fill="currentColor" opacity="0.8" />
    <circle cx="36" cy="36" r="4" fill="currentColor" opacity="0.8" />
    <circle cx="24" cy="24" r="5" fill="currentColor" />

    <path d="M12 12L24 24M36 12L24 24M12 36L24 24M36 36L24 24"
      stroke="currentColor"
      strokeWidth="1.5"
      opacity="0.4"
    />
  </svg>
)

// Upload Icon - Cloud with arrow
export const UploadIcon = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M32 20C32 15.5817 28.4183 12 24 12C20.2595 12 17.1049 14.6197 16.2368 18.1053C12.929 18.5553 10 21.3626 10 25C10 28.866 13.134 32 17 32H31C34.866 32 38 28.866 38 25C38 21.3626 35.071 18.5553 31.7632 18.1053"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
    />
    <path
      d="M24 24V38M24 24L20 28M24 24L28 28"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

// Export all icons
export default {
  SearchIcon,
  ProjectsIcon,
  ArchiveIcon,
  IndexIcon,
  AnalyticsIcon,
  SettingsIcon,
  VectorIcon,
  UploadIcon,
}
