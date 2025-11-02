# JavaScript/Node.js Standard Template

## package.json

```json
{
  "name": "$PROJECT_NAME",
  "version": "0.1.0",
  "description": "A JavaScript project",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write src/"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "@types/node": "^20.0.0"
  }
}
```

## src/index.js

```javascript
/**
 * Main entry point for $PROJECT_NAME
 */

function main() {
    console.log("Hello from $PROJECT_NAME!");
}

if (require.main === module) {
    main();
}

module.exports = { main };
```

## tests/index.test.js

```javascript
const { main } = require('../src/index');

describe('main function', () => {
    test('should run without errors', () => {
        expect(() => main()).not.toThrow();
    });
});
```

## Usage

This JavaScript setup provides:
- Modern package.json with npm scripts
- Jest for testing
- ESLint for linting
- Prettier for code formatting
- TypeScript type definitions
- Basic src/ structure

**Best for**: Node.js applications, JavaScript libraries, CLI tools
