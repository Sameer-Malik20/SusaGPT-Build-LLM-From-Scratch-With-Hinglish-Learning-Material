# 🅰️ Angular Enterprise Development - Complete Guide

> **Level:** Beginner → Expert | **Language:** Hinglish | **Goal:** Master Angular 17+ for enterprise applications with RxJS, TypeScript, and modern patterns.

---

## 🧭 Core Concepts (Concept-First)

- Angular Architecture: Modules, components, services
- TypeScript: Strong typing, decorators, generics
- RxJS: Observables, operators, reactive programming
- Dependency Injection: Tree-shakable providers
- Signals: Angular's new reactive primitive

---

## 📋 Complete Guide

### 1️⃣ Angular 17+ Fundamentals

**Standalone Components:**
```typescript
// main.ts
import { bootstrapApplication } from '@angular/platform-browser'
import { AppComponent } from './app/app.component'

bootstrapApplication(AppComponent, {
  providers: [provideRouter(routes)]
})
```

```typescript
// app.component.ts
import { Component } from '@angular/core'
import { CommonModule } from '@angular/common'

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h1>Hello {{ name }}</h1>
    <button (click)="onClick()">Click me</button>
  `
})
export class AppComponent {
  name = 'Angular 17'
  
  onClick() {
    console.log('Clicked!')
  }
}
```

### 2️⃣ Signals - Modern Reactivity

**Signal Basics:**
```typescript
import { signal, computed, effect } from '@angular/core'

// Primitive signal
const count = signal(0)

// Computed signal
const double = computed(() => count() * 2)

// Effect (automatic cleanup)
effect(() => {
  console.log('Count changed:', count())
})

// Update signal
count.set(5)
count.update(v => v + 1)
```

**Signal vs RxJS:**
```typescript
// Old way (RxJS)
name = new BehaviorSubject<string>('')

// New way (Signals)
name = signal('')

// Template me direct use
{{ name() }}
```

### 3️⃣ RxJS Deep Dive

**Common Operators:**
```typescript
import { of, interval, from } from 'rxjs'
import { map, filter, debounceTime, switchMap } from 'rxjs/operators'

// Search example
searchTerm.pipe(
  debounceTime(300),
  filter(term => term.length > 2),
  switchMap(term => http.get(`/search?q=${term}`))
).subscribe(results => this.results = results)

// Map & Filter
of(1, 2, 3, 4, 5).pipe(
  map(x => x * 2),
  filter(x => x > 5)
).subscribe(x => console.log(x)) // 6, 8, 10

// Combine streams
import { combineLatest, merge } from 'rxjs'
```

**Async Pipe:**
```typescript
@Component({
  template: `
    <li *ngFor="let item of items$ | async">
      {{ item.name }}
    </li>
  `
})
export class ListComponent {
  items$ = this.http.get<Item[]>('/api/items')
}
```

### 4️⃣ Dependency Injection

**Provider Scopes:**
```typescript
// Root level (singleton)
@Component({})
export class AppService {
  constructor(private http: HttpClient) {}
}

// Component level (new instance each time)
@Component({
  providers: [ComponentService]
})
export class MyComponent {
  constructor(private service: ComponentService) {}
}

// Factory provider
{
  provide: ApiService,
  useFactory: (http: HttpClient, config: Config) => {
    return new ApiService(http, config.apiUrl)
  },
  deps: [HttpClient, ConfigService]
}
```

### 5️⃣ Routing & Navigation

**Route Configuration:**
```typescript
// app.routes.ts
export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'dashboard',
    loadChildren: () => import('./dashboard/routes').then(m => m.DASHBOARD_ROUTES),
    canActivate: [authGuard]
  },
  {
    path: '**',
    loadComponent: () => import('./not-found/not-found.component').then(m => m.NotFoundComponent)
  }
]
```

**Router Hooks:**
```typescript
// Route guard
@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  canActivate(route: ActivatedRouteSnapshot) {
    return inject(AuthService).isLoggedIn()
  }
}

// Resolver
@Injectable({ providedIn: 'root' })
export class DataResolver implements Resolve<Data> {
  resolve(route: ActivatedRouteSnapshot) {
    return inject(DataService).getData(route.paramMap.get('id')!)
  }
}
```

### 6️⃣ State Management

**Services with Signals:**
```typescript
@Injectable({ providedIn: 'root' })
export class CartService {
  private items = signal<Product[]>([])
  
  cartItems = this.items.asReadonly()
  cartTotal = computed(() => 
    this.items().reduce((sum, item) => sum + item.price, 0)
  )
  
  addItem(product: Product) {
    this.items.update(items => [...items, product])
  }
  
  removeItem(productId: string) {
    this.items.update(items => items.filter(i => i.id !== productId))
  }
}
```

### 7️⃣ Performance Patterns

- **OnPush Change Detection:** `@ChangeDetectionStrategy.OnPush`
- **TrackBy Functions:** For `*ngFor` optimization
- **Lazy Loading:** Route-based code splitting
- **Deferrable Views:** `@defer` blocks
- **SSR with Hydration:** Angular Universal

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @defer (on viewport) {
      <heavy-component />
    } @placeholder {
      <skeleton-loader />
    }
  `
})
export class ParentComponent {}
```

---

## 🎯 Best Practices Checklist

- [ ] Use Standalone Components
- [ ] Prefer Signals over RxJS where possible
- [ ] Use OnPush change detection
- [ ] Implement proper lazy loading
- [ ] Write strict TypeScript
- [ ] Use Angular CLI for scaffolding

---

## 🔗 Related Resources

- [Angular Documentation](https://angular.dev)
- [Angular Signals Guide](https://angular.dev/guide/signals)
- [RxJS Operators](https://rxjs.dev/api)

---

> 💡 **Tip:** Angular 17+ mein bohot improvements hain. Signals use karo for better performance!