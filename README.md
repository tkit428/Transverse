# Transverse - Universal Translator

A minimalist, black and white translator website with modern design and smooth animations.

## Features

- **Clean Design**: Minimalist black and white interface with 14px rounded corners
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **File Upload**: Support for TXT, PDF, DOC, and DOCX files
- **Language Detection**: Auto-detect source language
- **Smooth Animations**: Powered by Anime.js with scroll observer
- **Copy & Speak**: Copy translations and text-to-speech functionality
- **Keyboard Shortcuts**: Fast translation with Ctrl/Cmd + Enter

## Navigation

- **Home**: Main translation interface
- **Features**: Overview of capabilities
- **Pricing**: Subscription plans
- **FAQ**: Frequently asked questions
- **GitHub**: Link to repository

## Usage

1. Open `index.html` in your browser
2. Select source and target languages
3. Enter text or upload a file
4. Click "Translate" or use Ctrl/Cmd + Enter
5. Copy or speak the translation

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Translate text
- `Ctrl/Cmd + K`: Focus input field
- `Escape`: Clear all text

## File Structure

```
/
├── index.html          # Main HTML file
├── styles.css          # CSS styles
├── script.js           # JavaScript functionality
├── icon/
│   ├── logo.svg        # Main logo
│   ├── web/            # Web icons
│   ├── android/        # Android icons
│   └── ios/            # iOS icons
└── README.md           # This file
```

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Interactive functionality
- **Anime.js**: Smooth animations
- **Intersection Observer API**: Scroll-based animations

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

To customize the translation functionality, modify the `simulateTranslation` function in `script.js` to integrate with your preferred translation API (Google Translate, Azure Translator, etc.).

## License

MIT License - feel free to use and modify as needed.
