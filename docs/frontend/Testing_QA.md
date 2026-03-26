# 🧪 Testing & Quality Assurance - Reliable Frontend Applications
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Frontend testing strategies, tools, aur quality assurance master karna

---

## 🧭 Core Concepts (Concept-First)

- Testing pyramid: unit, integration, end-to-end, visual tests.
- Key frameworks: Jest, Testing Library, Cypress, Playwright, Percy.
- Test strategy: deterministic tests, isolation, and fast feedback loops.
- Quality practices: accessibility checks, visual regression, and performance testing in CI.
- Metrics: coverage targets and bug prevention through tests.

---

## 📋 Table of Contents: Testing Pyramid

| Level | Test Type | Tools | Purpose |
|-------|-----------|-------|---------|
| **Unit Testing** | Component/Function tests | Jest, Vitest | Individual units test karna |
| **Integration Testing** | Component interaction | React Testing Library | Components integration test karna |
| **E2E Testing** | User workflow tests | Cypress, Playwright | Complete user journeys test karna |
| **Visual Testing** | UI appearance tests | Percy, Chromatic | Visual regressions detect karna |
| **Performance Testing** | Speed aur performance | Lighthouse, WebPageTest | Performance metrics measure karna |

---

## 1. 🧩 Unit Testing Fundamentals

### A. Jest Testing Framework

#### Basic Test Structure:
```javascript
// math.test.js
const { add, multiply, divide } = require('./math');

describe('Math operations', () => {
  test('adds two numbers correctly', () => {
    expect(add(2, 3)).toBe(5);
    expect(add(-1, 1)).toBe(0);
    expect(add(0, 0)).toBe(0);
  });

  test('multiplies two numbers correctly', () => {
    expect(multiply(2, 3)).toBe(6);
    expect(multiply(-2, 3)).toBe(-6);
  });

  test('throws error when dividing by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });
});
```

#### Mocking Dependencies:
```javascript
// api.test.js
const { fetchUser } = require('./api');
const axios = require('axios');

jest.mock('axios');

test('fetches user data successfully', async () => {
  const mockUser = { id: 1, name: 'John Doe' };
  axios.get.mockResolvedValue({ data: mockUser });

  const user = await fetchUser(1);
  
  expect(axios.get).toHaveBeenCalledWith('/api/users/1');
  expect(user).toEqual(mockUser);
});

test('handles API errors', async () => {
  axios.get.mockRejectedValue(new Error('Network error'));
  
  await expect(fetchUser(1)).rejects.toThrow('Network error');
});
```

### B. React Component Testing

#### Component Testing with Testing Library:
```javascript
// Button.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

test('renders button with correct text', () => {
  render(<Button>Click me</Button>);
  const button = screen.getByRole('button', { name: /click me/i });
  expect(button).toBeInTheDocument();
});

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click me</Button>);
  
  const button = screen.getByRole('button');
  fireEvent.click(button);
  
  expect(handleClick).toHaveBeenCalledTimes(1);
});

test('displays loading state', () => {
  render(<Button loading>Click me</Button>);
  const button = screen.getByRole('button');
  expect(button).toBeDisabled();
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
```

---

## 2. 🔗 Integration Testing

### A. Component Integration Tests

#### Testing Component Interactions:
```javascript
// LoginForm.test.jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from './LoginForm';
import { login } from './api';

jest.mock('./api');

test('submits form with correct data', async () => {
  const mockLogin = login.mockResolvedValue({ success: true });
  const onSuccess = jest.fn();
  
  render(<LoginForm onSuccess={onSuccess} />);
  
  // Fill form
  await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  
  // Submit form
  fireEvent.click(screen.getByRole('button', { name: /login/i }));
  
  // Verify API call
  await waitFor(() => {
    expect(mockLogin).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
  
  // Verify success callback
  expect(onSuccess).toHaveBeenCalled();
});

test('displays error message on failed login', async () => {
  login.mockRejectedValue(new Error('Invalid credentials'));
  
  render(<LoginForm />);
  
  await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'wrongpassword');
  fireEvent.click(screen.getByRole('button', { name: /login/i }));
  
  await waitFor(() => {
    expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
  });
});
```

### B. Custom Hook Testing

#### Testing React Hooks:
```javascript
// useCounter.test.js
import { renderHook, act } from '@testing-library/react';
import useCounter from './useCounter';

test('should use counter', () => {
  const { result } = renderHook(() => useCounter());
  
  expect(result.current.count).toBe(0);
  expect(typeof result.current.increment).toBe('function');
  expect(typeof result.current.decrement).toBe('function');
  expect(typeof result.current.reset).toBe('function');
});

test('should increment counter', () => {
  const { result } = renderHook(() => useCounter());
  
  act(() => {
    result.current.increment();
  });
  
  expect(result.current.count).toBe(1);
});

test('should accept initial value', () => {
  const { result } = renderHook(() => useCounter(10));
  
  expect(result.current.count).toBe(10);
});
```

---

## 3. 🌐 End-to-End Testing

### A. Cypress E2E Testing

#### Complete User Flow Test:
```javascript
// cypress/e2e/login.cy.js
describe('Login Flow', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login successfully with valid credentials', () => {
    // Intercept API call
    cy.intercept('POST', '/api/login', {
      statusCode: 200,
      body: { success: true, user: { name: 'John Doe' } }
    }).as('loginRequest');

    // Fill and submit form
    cy.get('[data-testid="email"]').type('test@example.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="login-button"]').click();

    // Verify API call
    cy.wait('@loginRequest');

    // Verify redirect and user data
    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="welcome-message"]').should('contain', 'John Doe');
  });

  it('should show error with invalid credentials', () => {
    cy.intercept('POST', '/api/login', {
      statusCode: 401,
      body: { error: 'Invalid credentials' }
    }).as('loginRequest');

    cy.get('[data-testid="email"]').type('wrong@example.com');
    cy.get('[data-testid="password"]').type('wrongpassword');
    cy.get('[data-testid="login-button"]').click();

    cy.wait('@loginRequest');
    cy.get('[data-testid="error-message"]').should('contain', 'Invalid credentials');
  });
});
```

#### E2E Testing Best Practices:
```javascript
// Custom commands for reusable actions
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="login-button"]').click();
});

Cypress.Commands.add('logout', () => {
  cy.get('[data-testid="user-menu"]').click();
  cy.get('[data-testid="logout-button"]').click();
});

// Using custom commands
it('should complete user journey', () => {
  cy.login('test@example.com', 'password123');
  // ... test actions
  cy.logout();
});
```

### B. Playwright E2E Testing

#### Cross-browser Testing:
```javascript
// playwright.config.js
module.exports = {
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    video: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
};

// test.spec.js
test('should work across browsers', async ({ page }) => {
  await page.goto('https://example.com');
  await page.click('button');
  await expect(page.locator('result')).toContainText('Success');
});
```

---

## 4. 🎨 Visual Testing

### A. Visual Regression Testing

#### Percy Integration:
```javascript
// percy.config.js
module.exports = {
  version: 2,
  snapshot: {
    widths: [1280, 768, 375], // Different screen sizes
    minHeight: 1024,
    percyCSS: `
      .ads { display: none; }
      .animations { animation: none; }
    `,
  },
  discovery: {
    allowedHostnames: ['example.com'],
    networkIdleTimeout: 250,
  },
};

// Visual test with Cypress
it('should match visual snapshot', () => {
  cy.visit('/dashboard');
  cy.percySnapshot('Dashboard Page');
  
  // Test different states
  cy.get('[data-testid="toggle-theme"]').click();
  cy.percySnapshot('Dashboard Page - Dark Mode');
});
```

#### Chromatic for Storybook:
```javascript
// .storybook/main.js
module.exports = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
  ],
  framework: '@storybook/react',
};

// Component story for visual testing
export const PrimaryButton = {
  args: {
    primary: true,
    label: 'Button',
  },
};

export const SecondaryButton = {
  args: {
    primary: false,
    label: 'Button',
  },
};
```

---

## 5. ⚡ Performance Testing

### A. Performance Metrics Testing

#### Lighthouse CI Integration:
```javascript
// lighthouse.config.js
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
      url: ['http://localhost:3000'],
      settings: {
        chromeFlags: '--no-sandbox',
      },
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.9 }],
        'categories:seo': ['warn', { minScore: 0.9 }],
        'first-contentful-paint': ['warn', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 4000 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
  },
};
```

#### Performance Budget Testing:
```javascript
// performance-budget.js
module.exports = {
  budgets: [
    {
      path: '/*',
      resourceSizes: [
        {
          resourceType: 'document',
          budget: 20, // 20KB
        },
        {
          resourceType: 'script',
          budget: 300, // 300KB
        },
        {
          resourceType: 'image',
          budget: 200, // 200KB
        },
      ],
      resourceCounts: [
        {
          resourceType: 'script',
          budget: 10, // Max 10 scripts
        },
      ],
    },
  ],
};
```

---

## 6. 🔧 Testing Strategy & Best Practices

### A. Test Organization

#### Test File Structure:
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.jsx
│   │   ├── Button.test.jsx
│   │   └── Button.stories.jsx
│   └── Form/
│       ├── Form.jsx
│       ├── Form.test.jsx
│       └── Form.stories.jsx
├── hooks/
│   ├── useCounter.js
│   └── useCounter.test.js
├── utils/
│   ├── api.js
│   └── api.test.js
└── __tests__/
    └── integration/  # Integration tests
```

#### Test Naming Conventions:
```javascript
// Good test names
describe('LoginForm', () => {
  test('should display error when email is invalid', () => {});
  test('should submit form with valid data', () => {});
  test('should show loading state during submission', () => {});
});

// Avoid vague names
describe('LoginForm', () => {
  test('test 1', () => {}); // ❌ Bad
  test('works', () => {});  // ❌ Bad
});
```

### B. Continuous Testing

#### GitHub Actions Workflow:
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm test -- --coverage --watchAll=false
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
      
      - name: Visual testing
        run: npm run test:visual
```

---

## 7. 🧪 Practical Testing Exercises

### Exercise 1: Component Testing
1. Complex React component create karo
2. Unit tests likho individual behaviors ke liye
3. Integration tests likho component interactions ke liye
4. Test coverage 90%+ achieve karo

### Exercise 2: E2E Testing
1. Complete user flow identify karo (login → action → logout)
2. Cypress tests likho complete flow ke liye
3. Cross-browser testing implement karo
4. Visual regression tests add karo

### Exercise 3: Performance Testing
1. Performance budget define karo
2. Lighthouse CI setup karo
3. Performance regression tests implement karo
4. Optimization opportunities identify karo

---

## 📚 Resources

### Testing Frameworks
- **Jest:** JavaScript testing framework
- **Testing Library:** DOM testing utilities
- **Cypress:** E2E testing framework
- **Playwright:** Cross-browser testing

### Visual Testing
- **Percy:** Visual testing platform
- **Chromatic:** Storybook visual testing
- **Applitools:** AI-powered visual testing

### Performance Testing
- **Lighthouse:** Web performance auditing
- **WebPageTest:** Advanced performance testing
- **PageSpeed Insights:** Google's performance tool

---

## 🏆 Checklist
- [ ] Unit testing frameworks use kar sakte hain
- [ ] Component integration testing implement kar sakte hain
- [ ] E2E testing strategies apply kar sakte hain
- [ ] Visual regression testing setup kar sakte hain
- [ ] Performance testing conduct kar sakte hain
- [ ] Testing best practices follow kar sakte hain
- [ ] Continuous testing pipelines create kar sakte hain

> **Pro Tip:** Testing pyramid follow karo - more unit tests, fewer integration tests, even fewer E2E tests. Tests should be fast, reliable, aur maintainable. Always test behavior, not implementation.
