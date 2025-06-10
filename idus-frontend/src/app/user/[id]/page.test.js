import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import UserDetails from './page';

jest.mock('../../components/LocationMap', () => ({ LocationMap: () => <div>Mapa</div> }));
jest.mock('../../components/PointsList', () => ({ PointsList: () => <div>Points</div> }));
jest.mock('../../components/DailySummary', () => ({ DailySummary: () => <div>Resumo</div> }));
jest.mock('../../components/RegisterPointModal', () => ({ RegisterPointModal: () => <div>Modal</div> }));
jest.mock('../../components/EditUserModal', () => ({ EditUserModal: () => <div>EditModal</div> }));
jest.mock('../../components/UserInfo', () => ({ UserInfo: ({ user }) => <div>{user.name}</div> }));

jest.mock('../../api/user', () => ({
  registerPoint: jest.fn(),
  getDailySummary: jest.fn(),
  registerPointManual: jest.fn(),
  getUserInfo: jest.fn(),
  updateUser: jest.fn(),
}));

jest.mock('next/navigation', () => ({
  useParams: () => ({ id: '1' }),
}));

const { getUserInfo, getDailySummary } = require('../../api/user');

describe('UserDetails', () => {
  it('carrega e exibe informacoes do usuario', async () => {
    getUserInfo.mockResolvedValue({
      first_name: 'John',
      last_name: 'Doe',
      cpf: '123',
      email: 'john@example.com',
      birth_date: '1990-01-01',
      work_schedule: '40h',
      role: 'admin',
    });

    getDailySummary.mockResolvedValue({ points: [] });

    render(<UserDetails />);

    await waitFor(() => expect(getUserInfo).toHaveBeenCalled());

    // abrir aba de informações
    fireEvent.click(screen.getByText('Informações'));

    expect(await screen.findByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Informações do Usuário')).toBeInTheDocument();
  });
});
