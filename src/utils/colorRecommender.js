// Color theory based recommender
export const getColorRecommendations = (rgbColor) => {
  const [r, g, b] = rgbColor.match(/\d+/g).map(Number);
  const [h, s, l] = rgbToHsl(r, g, b);

  // Get complementary color (opposite on the color wheel)
  const complementary = hslToRgb((h + 180) % 360, s, l);

  // Get triadic colors (three colors equally spaced on the color wheel)
  const triadic1 = hslToRgb((h + 120) % 360, s, l);
  const triadic2 = hslToRgb((h + 240) % 360, s, l);

  // Get split-complementary colors (one base color and two colors adjacent to its complement)
  const splitComp1 = hslToRgb((h + 150) % 360, s, l);
  const splitComp2 = hslToRgb((h + 210) % 360, s, l);

  // Get analogous colors (colors adjacent to the base color)
  const analogous1 = hslToRgb((h + 30) % 360, s, l);
  const analogous2 = hslToRgb((h - 30 + 360) % 360, s, l);

  // Get monochromatic variations
  const monochromatic1 = hslToRgb(h, Math.min(s + 0.2, 1), l);
  const monochromatic2 = hslToRgb(h, Math.max(s - 0.2, 0), l);

  return {
    complementary,
    triadic: [triadic1, triadic2],
    splitComplementary: [splitComp1, splitComp2],
    analogous: [analogous1, analogous2],
    monochromatic: [monochromatic1, monochromatic2]
  };
};

// Helper functions for color conversion
const rgbToHsl = (r, g, b) => {
  r /= 255;
  g /= 255;
  b /= 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h, s, l = (max + min) / 2;

  if (max === min) {
    h = s = 0;
  } else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      case b: h = (r - g) / d + 4; break;
    }

    h /= 6;
  }

  return [h * 360, s, l];
};

const hslToRgb = (h, s, l) => {
  h /= 360;
  let r, g, b;

  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;

    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }

  return `rgb(${Math.round(r * 255)},${Math.round(g * 255)},${Math.round(b * 255)})`;
};

// Get color name from RGB
export const getColorName = (rgbColor) => {
  const [r, g, b] = rgbColor.match(/\d+/g).map(Number);
  
  const colors = {
    'red': [255, 0, 0],
    'crimson': [220, 20, 60],
    'maroon': [128, 0, 0],
    'pink': [255, 192, 203],
    'orange': [255, 165, 0],
    'yellow': [255, 255, 0],
    'green': [0, 128, 0],
    'teal': [0, 128, 128],
    'blue': [0, 0, 255],
    'navy': [0, 0, 128],
    'purple': [128, 0, 128],
    'violet': [238, 130, 238],
    'brown': [165, 42, 42],
    'beige': [245, 245, 220],
    'white': [255, 255, 255],
    'gray': [128, 128, 128],
    'black': [0, 0, 0]
  };
  
  let closestColor = 'Unknown';
  let minDistance = Infinity;
  
  for (const [name, [cr, cg, cb]] of Object.entries(colors)) {
    const distance = Math.sqrt(
      Math.pow(r - cr, 2) +
      Math.pow(g - cg, 2) +
      Math.pow(b - cb, 2)
    );
    
    if (distance < minDistance) {
      minDistance = distance;
      closestColor = name;
    }
  }
  
  return closestColor;
}; 