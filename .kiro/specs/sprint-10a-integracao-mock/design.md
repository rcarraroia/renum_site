# SPRINT 10A - INTEGRAÇÃO MOCK → REAL - DESIGN

## 🏗️ ARQUITETURA GERAL

### Padrão de Integração
```
PÁGINA (React) → SERVICE (TypeScript) → API (FastAPI) → SUPABASE (PostgreSQL)
```

### Fluxo de Dados
```
1. Página carrega → useEffect()
2. Chama service.getAll()
3. Service faz HTTP request
4. Backend consulta Supabase
5. Dados retornam pela cadeia
6. Página atualiza estado
7. Interface renderiza dados reais
```

---

## 📂 ESTRUTURA DE ARQUIVOS

### Services Existentes (Reutilizar)
```
src/services/
├── leadService.ts          ✅ Existe - usar
├── clientService.ts        ✅ Existe - usar  
├── interviewService.ts     ✅ Existe - usar
├── reportService.ts        ✅ Existe - usar
├── agentService.ts         ✅ Existe - usar
├── siccService.ts          ✅ Existe - usar
└── conversationService.ts  ✅ Existe - usar
```

### Services a Criar
```
src/services/
├── configService.ts        ❌ Criar - para configurações
├── settingsService.ts      ❌ Criar - para settings
└── aiService.ts           ❌ Criar - para assistente ISA
```

### Páginas a Modificar (14 páginas)
```
src/pages/dashboard/
├── AdminClientsPage.tsx                   🔄 Conectar ao clientService
├── AdminLeadsPage.tsx                     🔄 Conectar ao leadService (versão antiga)
├── AdminReportsPage.tsx                   🔄 Conectar ao reportService
├── PesquisasAnalisePage.tsx               🔄 Conectar ao interviewService
├── PesquisasEntrevistasPage.tsx           🔄 Conectar ao interviewService
├── PesquisasResultadosPage.tsx            🔄 Conectar ao interviewService
├── ClientOverview.tsx                     🔄 Conectar ao dashboardService
├── RenusConfigPage.tsx                    🔄 Conectar ao configService
└── AssistenteIsaPage.tsx                  🔄 Conectar ao AI service

src/pages/sicc/
├── EvolutionPage.tsx                      🔄 Hardcoded → siccService
├── LearningQueuePage.tsx                  🔄 Hardcoded → siccService
├── MemoryManagerPage.tsx                  🔄 Hardcoded → siccService
└── SettingsPage.tsx                       🔄 Hardcoded → siccService
```

### Arquivos Mock a Deletar (após migração)
```
src/data/
├── mockReports.ts                         🗑️ Deletar (17 constantes MOCK_)
├── mockProjects.ts                        🗑️ Deletar (3 constantes MOCK_)
└── mockConversations.ts                   🗑️ Deletar (4 constantes MOCK_)
```

### Páginas JÁ Conectadas (não modificar)
```
src/pages/dashboard/
├── AdminOverview.tsx                      ✅ Usa dashboardService
├── AdminProjectsPage.tsx                  ✅ Usa projectService
├── AdminConversationsPage.tsx             ✅ Usa conversationService
└── AdminLeadsPageNew.tsx                  ✅ Usa leadService

src/pages/agents/
├── AgentsPage.tsx                         ✅ Usa agentService
├── AgentDetailPage.tsx                    ✅ Usa agentService
└── SubAgentsPage.tsx                      ✅ Usa agentService

src/pages/admin/agents/
├── AgentCreatePage.tsx                    ✅ JÁ EXISTE
├── AgentDetailsPage.tsx                   ✅ JÁ EXISTE
└── AgentsListPage.tsx                     ✅ JÁ EXISTE
```

---

## 🔄 PADRÕES DE CONVERSÃO

### Padrão 1: Substituição Direta de Mock
```typescript
// ANTES (Mock)
const [leads, setLeads] = useState(MOCK_LEADS);

// DEPOIS (Real)
const [leads, setLeads] = useState<Lead[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
  const loadLeads = async () => {
    try {
      setLoading(true);
      const data = await leadService.getAll();
      setLeads(data.items);
    } catch (err) {
      setError('Erro ao carregar leads');
    } finally {
      setLoading(false);
    }
  };
  
  loadLeads();
}, []);
```

### Padrão 2: Estados de Loading
```typescript
// Estados obrigatórios para todas as páginas
interface PageState<T> {
  data: T[];
  loading: boolean;
  error: string | null;
  page: number;
  totalPages: number;
}

// Hook customizado reutilizável
const usePageData = <T>(service: any, deps: any[] = []) => {
  const [state, setState] = useState<PageState<T>>({
    data: [],
    loading: true,
    error: null,
    page: 1,
    totalPages: 1
  });
  
  // Lógica de carregamento...
  
  return { ...state, refetch };
};
```

### Padrão 3: Tratamento de Erros
```typescript
// Componente de erro reutilizável
const ErrorMessage = ({ error, onRetry }: { error: string; onRetry: () => void }) => (
  <div className="error-container">
    <p>{error}</p>
    <button onClick={onRetry}>Tentar Novamente</button>
  </div>
);

// Loading skeleton reutilizável
const LoadingSkeleton = ({ rows = 5 }: { rows?: number }) => (
  <div className="loading-skeleton">
    {Array.from({ length: rows }).map((_, i) => (
      <div key={i} className="skeleton-row" />
    ))}
  </div>
);
```

---

## 🎨 COMPONENTES REUTILIZÁVEIS

### DataTable Genérico
```typescript
interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  loading: boolean;
  error: string | null;
  onRetry: () => void;
  pagination?: PaginationProps;
}

const DataTable = <T,>({ data, columns, loading, error, onRetry, pagination }: DataTableProps<T>) => {
  if (loading) return <LoadingSkeleton />;
  if (error) return <ErrorMessage error={error} onRetry={onRetry} />;
  
  return (
    <div className="data-table">
      <table>
        <thead>
          {columns.map(col => <th key={col.key}>{col.title}</th>)}
        </thead>
        <tbody>
          {data.map((item, i) => (
            <tr key={i}>
              {columns.map(col => (
                <td key={col.key}>{col.render ? col.render(item) : item[col.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {pagination && <Pagination {...pagination} />}
    </div>
  );
};
```

### PageContainer Padrão
```typescript
interface PageContainerProps {
  title: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  loading?: boolean;
}

const PageContainer = ({ title, children, actions, loading }: PageContainerProps) => (
  <div className="page-container">
    <div className="page-header">
      <h1>{title}</h1>
      {actions && <div className="page-actions">{actions}</div>}
    </div>
    <div className="page-content">
      {loading ? <LoadingSkeleton /> : children}
    </div>
  </div>
);
```

---

## 🔌 INTEGRAÇÃO COM SERVICES

### Service Interface Padrão
```typescript
interface BaseService<T, CreateT, UpdateT> {
  getAll(params?: QueryParams): Promise<PaginatedResponse<T>>;
  getById(id: string): Promise<T>;
  create(data: CreateT): Promise<T>;
  update(id: string, data: UpdateT): Promise<T>;
  delete(id: string): Promise<void>;
}

interface QueryParams {
  page?: number;
  limit?: number;
  search?: string;
  filters?: Record<string, any>;
}

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  totalPages: number;
}
```

### Implementação de Service
```typescript
class LeadService implements BaseService<Lead, LeadCreate, LeadUpdate> {
  async getAll(params: QueryParams = {}): Promise<PaginatedResponse<Lead>> {
    const { data } = await apiClient.get<PaginatedResponse<Lead>>('/api/leads', params);
    return data;
  }
  
  async getById(id: string): Promise<Lead> {
    const { data } = await apiClient.get<Lead>(`/api/leads/${id}`);
    return data;
  }
  
  // ... outros métodos
}
```

---

## 📊 ESTRUTURA DE DADOS

### Tipos TypeScript Alinhados
```typescript
// Garantir que types frontend correspondem ao backend
interface Lead {
  id: string;
  name: string;
  email: string;
  phone: string;
  status: LeadStatus;
  stage: LeadStage;
  client_id: string;
  created_at: string;
  updated_at: string;
}

// Enums alinhados com backend
enum LeadStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  BLOCKED = 'blocked'
}

enum LeadStage {
  NEW = 'new',
  CONTACTED = 'contacted',
  QUALIFIED = 'qualified',
  CONVERTED = 'converted'
}
```

### Validação de Dados
```typescript
// Validação runtime com Zod (opcional)
import { z } from 'zod';

const LeadSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  phone: z.string().min(10),
  status: z.enum(['active', 'inactive', 'blocked']),
  stage: z.enum(['new', 'contacted', 'qualified', 'converted']),
  client_id: z.string().uuid(),
  created_at: z.string(),
  updated_at: z.string()
});

// Usar na validação de responses
const validateLead = (data: unknown): Lead => {
  return LeadSchema.parse(data);
};
```

---

## 🎯 OTIMIZAÇÕES DE PERFORMANCE

### Lazy Loading de Páginas
```typescript
// Carregar páginas sob demanda
const LeadsPage = lazy(() => import('./pages/leads/LeadsPage'));
const ClientsPage = lazy(() => import('./pages/clients/ClientsPage'));

// No router
<Route path="/leads" element={
  <Suspense fallback={<LoadingSkeleton />}>
    <LeadsPage />
  </Suspense>
} />
```

### Cache de Dados
```typescript
// Cache simples com React Query (opcional)
import { useQuery } from '@tanstack/react-query';

const useLeads = (params: QueryParams) => {
  return useQuery({
    queryKey: ['leads', params],
    queryFn: () => leadService.getAll(params),
    staleTime: 5 * 60 * 1000, // 5 minutos
    cacheTime: 10 * 60 * 1000, // 10 minutos
  });
};
```

### Paginação Eficiente
```typescript
// Paginação server-side
const usePaginatedData = <T>(
  service: (params: QueryParams) => Promise<PaginatedResponse<T>>,
  initialParams: QueryParams = {}
) => {
  const [params, setParams] = useState(initialParams);
  const [data, setData] = useState<PaginatedResponse<T> | null>(null);
  const [loading, setLoading] = useState(true);
  
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const result = await service(params);
      setData(result);
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false);
    }
  }, [service, params]);
  
  useEffect(() => {
    loadData();
  }, [loadData]);
  
  return { data, loading, params, setParams, refetch: loadData };
};
```

---

## 🔒 CORRECTNESS PROPERTIES

### CP-01: Consistência de Dados
**Property:** ∀ página P, dados exibidos = dados do backend  
**Verification:** Comparar dados da página com response da API

### CP-02: Estados Válidos
**Property:** ∀ momento t, página está em estado válido (loading XOR data XOR error)  
**Verification:** Verificar que estados são mutuamente exclusivos

### CP-03: Sincronização
**Property:** ∀ operação CRUD, interface reflete mudança imediatamente  
**Verification:** Testar que create/update/delete atualizam lista

### CP-04: Tratamento de Erros
**Property:** ∀ erro E, usuário recebe feedback claro e ação de recovery  
**Verification:** Simular erros e verificar UX

### CP-05: Performance
**Property:** ∀ página P, tempo de carregamento ≤ 3 segundos  
**Verification:** Medir tempos de carregamento com dados reais

---

## 🧪 ESTRATÉGIA DE TESTES

### Testes Unitários
```typescript
// Testar services isoladamente
describe('LeadService', () => {
  it('should fetch leads successfully', async () => {
    const mockData = { items: [mockLead], total: 1, page: 1, totalPages: 1 };
    jest.spyOn(apiClient, 'get').mockResolvedValue({ data: mockData });
    
    const result = await leadService.getAll();
    
    expect(result).toEqual(mockData);
    expect(apiClient.get).toHaveBeenCalledWith('/api/leads', {});
  });
});
```

### Testes de Integração
```typescript
// Testar páginas com services reais
describe('LeadsPage Integration', () => {
  it('should load and display leads', async () => {
    render(<LeadsPage />);
    
    expect(screen.getByText('Carregando...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('João Silva')).toBeInTheDocument();
    });
    
    expect(screen.queryByText('Carregando...')).not.toBeInTheDocument();
  });
});
```

### Testes E2E
```typescript
// Testar fluxos completos
describe('Lead Management E2E', () => {
  it('should create, edit and delete lead', async () => {
    // 1. Navegar para página de leads
    await page.goto('/leads');
    
    // 2. Criar novo lead
    await page.click('[data-testid="create-lead-btn"]');
    await page.fill('[name="name"]', 'Novo Lead');
    await page.click('[data-testid="save-btn"]');
    
    // 3. Verificar que apareceu na lista
    await expect(page.locator('text=Novo Lead')).toBeVisible();
    
    // 4. Editar lead
    await page.click('[data-testid="edit-lead-btn"]');
    await page.fill('[name="name"]', 'Lead Editado');
    await page.click('[data-testid="save-btn"]');
    
    // 5. Verificar edição
    await expect(page.locator('text=Lead Editado')).toBeVisible();
    
    // 6. Deletar lead
    await page.click('[data-testid="delete-lead-btn"]');
    await page.click('[data-testid="confirm-delete-btn"]');
    
    // 7. Verificar que foi removido
    await expect(page.locator('text=Lead Editado')).not.toBeVisible();
  });
});
```

---

**Versão:** 1.0  
**Data:** 2025-12-10  
**Responsável:** Kiro (Agente de IA)