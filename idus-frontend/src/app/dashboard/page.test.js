import { render, screen, waitFor } from '@testing-library/react';
import Dashboard from './page';

jest.mock('../api/user', () => ({
  fetchUsers: jest.fn(),
}));

jest.mock('../api/auth', () => ({
  logout: jest.fn(),
}));

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: jest.fn() }),
}));

const { fetchUsers } = require('../api/user');

describe('Dashboard', () => {
  it('lista usuarios e mostra botoes de administracao', async () => {
    fetchUsers.mockResolvedValue({
      data: [
        { id: 1, first_name: 'John', last_name: 'Doe', role: 'admin', work_schedule: '40h' },
      ],
    });

    render(<Dashboard />);

    await waitFor(() => expect(fetchUsers).toHaveBeenCalled());

    expect(screen.getByText('Usuários')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Criar Novo Usuário')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });
});
