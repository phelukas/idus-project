import { render, screen } from '@testing-library/react';
import { UserInfo } from './UserInfo';

describe('UserInfo', () => {
  it('exibe informacoes do usuario', () => {
    const user = {
      name: 'Joao Silva',
      cpf: '123.456.789-00',
      email: 'joao@example.com',
      birthDate: '1990-01-01',
      workload: '40h',
      role: 'admin',
    };

    render(<UserInfo user={user} />);

    expect(screen.getByText(/Joao Silva/)).toBeInTheDocument();
    expect(screen.getByText('123.456.789-00')).toBeInTheDocument();
    expect(screen.getByText('joao@example.com')).toBeInTheDocument();
    expect(screen.getByText('1990-01-01')).toBeInTheDocument();
    expect(screen.getByText('40h')).toBeInTheDocument();
    expect(screen.getByText('Administrador')).toBeInTheDocument();
  });
});
