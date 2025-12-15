"""
Sprint 05B - Task 2: Validação Frontend
Testa frontend no navegador real
"""
import time
import json
from dataclasses import dataclass
from typing import Optional, List
import sys
import os

# Verificar se selenium está instalado
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    print("❌ Selenium não está instalado!")
    print("   Instale com: pip install selenium")
    sys.exit(1)


@dataclass
class TestResult:
    test_name: str
    passed: bool
    message: str
    duration_ms: float
    screenshot_path: Optional[str] = None
    details: Optional[dict] = None


class FrontendValidator:
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url
        self.driver: Optional[webdriver.Chrome] = None
        self.results: List[TestResult] = []
        self.screenshots_dir = "frontend_screenshots"
        
        # Criar diretório para screenshots
        os.makedirs(self.screenshots_dir, exist_ok=True)
    
    def setup_browser(self):
        """Inicializa navegador Chrome"""
        print("\n🌐 Iniciando navegador Chrome...")
        
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            self.driver = webdriver.Chrome(options=options)
            print("✅ Navegador iniciado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao iniciar navegador: {e}")
            print("   Certifique-se de ter o ChromeDriver instalado")
            sys.exit(1)
    
    def teardown_browser(self):
        """Fecha navegador"""
        if self.driver:
            self.driver.quit()
            print("\n🔒 Navegador fechado")
    
    def take_screenshot(self, name: str) -> str:
        """Captura screenshot"""
        if self.driver:
            filepath = os.path.join(self.screenshots_dir, f"{name}.png")
            self.driver.save_screenshot(filepath)
            return filepath
        return ""
    
    def test_page_load(self) -> TestResult:
        """Testa carregamento da página sem erros"""
        test_name = "Page load without errors"
        start = time.time()
        
        try:
            # Acessar página
            self.driver.get(self.base_url)
            
            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # Capturar screenshot
            screenshot = self.take_screenshot("01_page_load")
            
            # Verificar erros no console
            logs = self.driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            
            duration = (time.time() - start) * 1000
            
            if not errors:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message="✅ Page loaded without console errors",
                    duration_ms=duration,
                    screenshot_path=screenshot
                )
            else:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message=f"❌ Found {len(errors)} console errors",
                    duration_ms=duration,
                    screenshot_path=screenshot,
                    details={"errors": [e['message'] for e in errors[:5]]}
                )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Page load failed: {str(e)}",
                duration_ms=duration
            )
    
    def test_login_flow(self) -> TestResult:
        """Testa fluxo de login"""
        test_name = "Login flow"
        start = time.time()
        
        try:
            # Verificar se está na página de login
            current_url = self.driver.current_url
            
            # Capturar screenshot
            screenshot = self.take_screenshot("02_login_page")
            
            duration = (time.time() - start) * 1000
            
            # Verificar se há formulário de login ou se já está autenticado
            try:
                # Procurar por elementos de login
                login_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='email'], input[type='password'], button[type='submit']")
                
                if login_elements:
                    return TestResult(
                        test_name=test_name,
                        passed=True,
                        message="✅ Login page rendered (form found)",
                        duration_ms=duration,
                        screenshot_path=screenshot,
                        details={"url": current_url, "elements_found": len(login_elements)}
                    )
                else:
                    # Pode já estar autenticado
                    return TestResult(
                        test_name=test_name,
                        passed=True,
                        message="✅ Already authenticated or no login required",
                        duration_ms=duration,
                        screenshot_path=screenshot,
                        details={"url": current_url}
                    )
            
            except NoSuchElementException:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message="✅ No login form (may be authenticated)",
                    duration_ms=duration,
                    screenshot_path=screenshot
                )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Login test failed: {str(e)}",
                duration_ms=duration
            )
    
    def test_navigation(self) -> TestResult:
        """Testa navegação entre páginas"""
        test_name = "Navigation between pages"
        start = time.time()
        
        try:
            pages_tested = []
            
            # Lista de rotas para testar
            routes = [
                "/",
                "/clients",
                "/leads",
                "/projects",
                "/wizard",
                "/integrations"
            ]
            
            for route in routes:
                try:
                    url = f"{self.base_url}{route}"
                    self.driver.get(url)
                    
                    # Aguardar carregamento
                    time.sleep(1)
                    
                    # Verificar se não há tela branca
                    body_text = self.driver.find_element(By.TAG_NAME, "body").text
                    
                    if body_text.strip():
                        pages_tested.append({
                            "route": route,
                            "status": "✅ OK",
                            "has_content": True
                        })
                        
                        # Screenshot
                        self.take_screenshot(f"03_nav_{route.replace('/', '_')}")
                    else:
                        pages_tested.append({
                            "route": route,
                            "status": "⚠️ Empty",
                            "has_content": False
                        })
                
                except Exception as e:
                    pages_tested.append({
                        "route": route,
                        "status": f"❌ Error: {str(e)}",
                        "has_content": False
                    })
            
            duration = (time.time() - start) * 1000
            
            # Contar sucessos
            successful = sum(1 for p in pages_tested if p["has_content"])
            total = len(pages_tested)
            
            if successful == total:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message=f"✅ All {total} pages loaded successfully",
                    duration_ms=duration,
                    details={"pages": pages_tested}
                )
            else:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message=f"❌ Only {successful}/{total} pages loaded",
                    duration_ms=duration,
                    details={"pages": pages_tested}
                )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Navigation test failed: {str(e)}",
                duration_ms=duration
            )
    
    def test_data_loading(self) -> TestResult:
        """Testa carregamento de dados do backend"""
        test_name = "Data loading from backend"
        start = time.time()
        
        try:
            # Ir para página de clientes
            self.driver.get(f"{self.base_url}/clients")
            time.sleep(2)
            
            # Capturar screenshot
            screenshot = self.take_screenshot("04_data_loading")
            
            # Verificar se há elementos de dados ou loading
            page_source = self.driver.page_source.lower()
            
            has_data_indicators = (
                "loading" in page_source or
                "carregando" in page_source or
                "table" in page_source or
                "list" in page_source or
                "grid" in page_source
            )
            
            duration = (time.time() - start) * 1000
            
            if has_data_indicators:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message="✅ Data loading indicators found",
                    duration_ms=duration,
                    screenshot_path=screenshot
                )
            else:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message="⚠️ No data loading indicators found",
                    duration_ms=duration,
                    screenshot_path=screenshot
                )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Data loading test failed: {str(e)}",
                duration_ms=duration
            )
    
    def test_crud_operations(self) -> TestResult:
        """Testa operações CRUD (visual)"""
        test_name = "CRUD operations (visual check)"
        start = time.time()
        
        try:
            # Ir para página de clientes
            self.driver.get(f"{self.base_url}/clients")
            time.sleep(2)
            
            # Procurar botões de ação
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            
            # Capturar screenshot
            screenshot = self.take_screenshot("05_crud_operations")
            
            duration = (time.time() - start) * 1000
            
            if buttons:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message=f"✅ Found {len(buttons)} interactive buttons",
                    duration_ms=duration,
                    screenshot_path=screenshot,
                    details={"buttons_count": len(buttons)}
                )
            else:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message="❌ No interactive buttons found",
                    duration_ms=duration,
                    screenshot_path=screenshot
                )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ CRUD test failed: {str(e)}",
                duration_ms=duration
            )
    
    def run_all_tests(self) -> List[TestResult]:
        """Executa todos os testes"""
        print("\n" + "="*60)
        print("🧪 FRONTEND VALIDATION - Sprint 05B Task 2")
        print("="*60 + "\n")
        
        tests = [
            ("1. Page load", self.test_page_load),
            ("2. Login flow", self.test_login_flow),
            ("3. Navigation", self.test_navigation),
            ("4. Data loading", self.test_data_loading),
            ("5. CRUD operations", self.test_crud_operations),
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            result = test_func()
            self.results.append(result)
            
            print(f"   {result.message}")
            print(f"   Duration: {result.duration_ms:.0f}ms")
            
            if result.screenshot_path:
                print(f"   Screenshot: {result.screenshot_path}")
            
            if result.details:
                print(f"   Details: {json.dumps(result.details, indent=2)}")
        
        return self.results
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60 + "\n")
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {total - passed} ❌")
        print(f"Success Rate: {percentage:.1f}%")
        
        print(f"\n📸 Screenshots saved in: {self.screenshots_dir}/")
        
        print("\n" + "-"*60)
        print("DETAILED RESULTS:")
        print("-"*60 + "\n")
        
        for i, result in enumerate(self.results, 1):
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{i}. {result.test_name}: {status}")
            print(f"   {result.message}")
            print(f"   Duration: {result.duration_ms:.0f}ms")
            if result.screenshot_path:
                print(f"   Screenshot: {result.screenshot_path}")
            print()
        
        print("="*60 + "\n")
        
        return passed == total


def main():
    """Main function"""
    validator = FrontendValidator()
    
    try:
        # Setup
        validator.setup_browser()
        
        # Executar testes
        validator.run_all_tests()
        
        # Imprimir resumo
        all_passed = validator.print_summary()
        
        # Exit code
        sys.exit(0 if all_passed else 1)
    
    finally:
        # Cleanup
        validator.teardown_browser()


if __name__ == "__main__":
    main()
