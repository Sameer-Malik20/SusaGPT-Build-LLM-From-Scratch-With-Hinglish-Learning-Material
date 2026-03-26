# 🚀 NestJS Microservices - Complete Guide

> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Master NestJS with modular architecture, GraphQL, and microservices patterns.

---

## 🧭 Core Concepts (Concept-First)

- NestJS Architecture: Modules, controllers, providers
- Dependency Injection: Hierarchical injectors
- Microservices: TCP, gRPC, Message Brokers
- GraphQL: Code-first approach with Apollo
- Guards & Interceptors: Authentication & logging
- WebSockets: Real-time communication

---

## 📋 Complete Guide

### 1️⃣ NestJS Fundamentals

**Module Structure:**
```typescript
// users.module.ts
import { Module } from '@nestjs/common'
import { UsersController } from './users.controller'
import { UsersService } from './users.service'
import { DatabaseModule } from '../database/database.module'

@Module({
  imports: [DatabaseModule],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService]
})
export class UsersModule {}
```

**Controller Pattern:**
```typescript
// users.controller.ts
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common'

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  findAll(@Query('page') page: string, @Query('limit') limit: string) {
    return this.usersService.findAll({ 
      page: +page || 1, 
      limit: +limit || 10 
    })
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id)
  }

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto)
  }
}
```

**Service with DTO:**
```typescript
// users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common'

@Injectable()
export class UsersService {
  private users: User[] = []

  create(createUserDto: CreateUserDto): User {
    const user: User = {
      id: crypto.randomUUID(),
      ...createUserDto,
      createdAt: new Date()
    }
    this.users.push(user)
    return user
  }

  findAll(pagination: PaginationParams): PaginatedResult<User> {
    const start = (pagination.page - 1) * pagination.limit
    const end = start + pagination.limit
    
    return {
      data: this.users.slice(start, end),
      total: this.users.length,
      page: pagination.page,
      limit: pagination.limit
    }
  }

  findOne(id: string): User {
    const user = this.users.find(u => u.id === id)
    if (!user) throw new NotFoundException(`User ${id} not found`)
    return user
  }
}
```

### 2️⃣ Dependency Injection Deep Dive

**Provider Types:**
```typescript
// Basic provider
@Injectable()
export class UsersService {}

// Factory provider
{
  provide: 'CONFIG',
  useFactory: async () => {
    const config = await loadConfig()
    return config
  }
}

// Alias provider
{
  provide: 'UserService',
  useClass: UsersService
}

// Value provider
{
  provide: 'APP_NAME',
  useValue: 'MyApp'
}

// Class provider
{
  provide: Logger,
  useClass: WinstonLogger
}
```

**Injection with Scopes:**
```typescript
// Request-scoped (new instance per request)
@Injectable({ scope: Scope.REQUEST })
export class UsersService {
  constructor(@Inject(REQUEST) private request: Request) {}
}

// Transient (new instance each time)
@Injectable({ scope: Scope.TRANSIENT })
export class AnalyticsService {}
```

### 3️⃣ GraphQL with NestJS

**Code-First Approach:**
```typescript
// user.model.ts
import { ObjectType, Field, ID } from '@nestjs/graphql'

@ObjectType()
export class User {
  @Field(() => ID)
  id: string

  @Field()
  name: string

  @Field()
  email: string

  @Field({ nullable: true })
  avatar?: string

  @Field()
  createdAt: Date
}

// user.resolver.ts
@Resolver(() => User)
export class UsersResolver {
  constructor(private usersService: UsersService) {}

  @Query(() => [User])
  async users(): Promise<User[]> {
    return this.usersService.findAll()
  }

  @Query(() => User, { nullable: true })
  async user(@Args('id') id: string): Promise<User> {
    return this.usersService.findOne(id)
  }

  @Mutation(() => User)
  async createUser(@Args('input') input: CreateUserInput): Promise<User> {
    return this.usersService.create(input)
  }

  @ResolveField()
  async fullName(@Parent() user: User): Promise<string> {
    return `${user.name}`
  }
}
```

**Module Setup:**
```typescript
@Module({
  imports: [
    GraphQLModule.forRoot<ApolloDriverConfig>({
      driver: ApolloDriver,
      autoSchemaFile: join(process.cwd(), 'src/schema.gql'),
      sortSchema: true
    }),
    UsersModule
  ]
})
export class AppModule {}
```

### 4️⃣ Microservices Architecture

**TCP Microservice:**
```typescript
// main.ts (User Service)
async function bootstrap() {
  const app = await NestFactory.createMicroservice(AppModule, {
    transport: Transport.TCP,
    options: { port: 3001 }
  })
  await app.listen()
}
bootstrap()

// controller.ts
@Controller()
export class UsersController {
  @MessagePattern({ cmd: 'get-user' })
  getUser(@Payload() data: { id: string }): User {
    return this.usersService.findOne(data.id)
  }

  @MessagePattern({ cmd: 'create-user' })
  createUser(@Payload() data: CreateUserDto): User {
    return this.usersService.create(data)
  }
}
```

**Gateway (Client):**
```typescript
@Client({
  transport: Transport.TCP,
  options: { host: 'localhost', port: 3001 }
})
client: ClientProxy

async getUser(id: string) {
  return this.client.send({ cmd: 'get-user' }, { id }).toPromise()
}
```

### 5️⃣ Guards & Interceptors

**Auth Guard:**
```typescript
@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest()
    const token = this.extractToken(request)
    
    if (!token) return false
    
    try {
      const payload = await this.jwtService.verifyAsync(token)
      request['user'] = payload
    } catch {
      return false
    }
    
    return true
  }

  private extractToken(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? []
    return type === 'Bearer' ? token : undefined
  }
}
```

**Logging Interceptor:**
```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now()
    return next
      .handle()
      .pipe(
        tap(() => console.log(`After... ${Date.now() - now}ms`)),
        catchError(err => {
          console.error('Error:', err)
          throw err
        })
      )
  }
}
```

### 6️⃣ Real-time with WebSockets

```typescript
@WebSocketGateway({ cors: true })
export class EventsGateway {
  @WebSocketServer()
  server: Server

  @SubscribeMessage('message')
  handleMessage(@MessageBody() data: string): string {
    this.server.emit('message', data)
    return 'Message sent!'
  }

  @SubscribeMessage('join-room')
  handleJoinRoom(
    @MessageBody() room: string,
    @ConnectedSocket() client: Socket
  ): void {
    client.join(room)
  }

  handleConnection(client: Socket): void {
    console.log(`Client connected: ${client.id}`)
  }
}
```

---

## 🎯 Best Practices Checklist

- [ ] Use Modular architecture
- [ ] Implement proper DTOs with validation
- [ ] Use Interceptors for cross-cutting concerns
- [ ] Implement proper error handling
- [ ] Use GraphQL for complex APIs
- [ ] Implement proper testing (unit & e2e)

---

## 🔗 Related Resources

- [NestJS Documentation](https://docs.nestjs.com)
- [NestJS GraphQL](https://docs.nestjs.com/graphql/quick-start)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

> 💡 **Tip:** NestJS ka modular architecture bohot powerful hai. Badges use karo for clean documentation!