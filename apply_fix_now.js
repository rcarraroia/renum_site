// Script para aplicar correção de autenticação imediatamente
// Execute este código no console do navegador (F12)

console.log('🔧 APLICANDO CORREÇÃO DE AUTENTICAÇÃO...');

// 1. Limpar dados antigos
localStorage.removeItem('renum_token');
localStorage.removeItem('renum_user');
console.log('✅ Dados antigos removidos');

// 2. Token válido gerado pelo backend
const validToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NTE2NzU5LCJpYXQiOjE3NjU0MzAzNTksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Dgavryf5gfGa2fj-FEts2GnzxHBHBO7v7O13mQaI9W0';

// 3. Dados do usuário admin
const validUser = {
  id: '876be331-9553-4e9a-9f29-63cfa711e056',
  name: 'Admin Renum',
  email: 'rcarraro2015@gmail.com',
  role: 'admin'
};

// 4. Aplicar correção
localStorage.setItem('renum_token', validToken);
localStorage.setItem('renum_user', JSON.stringify(validUser));

console.log('✅ Token válido aplicado:', validToken.substring(0, 50) + '...');
console.log('✅ Usuário definido:', validUser.name, '(' + validUser.role + ')');

// 5. Testar token
fetch('http://localhost:8000/api/dashboard/stats', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${validToken}`,
    'Content-Type': 'application/json'
  }
})
.then(response => {
  if (response.ok) {
    console.log('✅ SUCESSO! Backend respondeu com status:', response.status);
    return response.json();
  } else {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
})
.then(data => {
  console.log('✅ DADOS RECEBIDOS:', data);
  console.log('🎯 CORREÇÃO APLICADA COM SUCESSO!');
  console.log('🔄 Recarregando página...');
  
  // Recarregar página após 2 segundos
  setTimeout(() => {
    location.reload();
  }, 2000);
})
.catch(error => {
  console.error('❌ ERRO:', error);
  console.log('⚠️ Verifique se o backend está rodando na porta 8000');
});

console.log('📋 INSTRUÇÕES:');
console.log('1. Se viu "✅ SUCESSO!" acima, aguarde o reload automático');
console.log('2. Se viu "❌ ERRO", verifique se backend está rodando');
console.log('3. Após reload, o sistema deve funcionar normalmente');