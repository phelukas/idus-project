global.fetch = jest.fn();

describe('api/user', () => {
  beforeEach(() => {
    fetch.mockClear();
    process.env.NEXT_PUBLIC_API_URL = 'http://localhost';
    localStorage.setItem('access_token', 'token');
    jest.resetModules();
  });

  it('listUsers faz requisicao GET correta', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ result: 'ok' }),
      headers: { get: () => 'application/json' },
    });
    const { listUsers } = require('./user');
    const data = await listUsers();
    expect(fetch).toHaveBeenCalledWith('http://localhost/users/list/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer token',
      },
      body: null,
    });
    expect(data).toEqual({ result: 'ok' });
  });

  it('updateUser envia dados com PUT', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ done: true }),
      headers: { get: () => 'application/json' },
    });
    const { updateUser } = require('./user');
    const data = await updateUser(5, { name: 'test' });
    expect(fetch).toHaveBeenCalledWith('http://localhost/users/update/5/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer token',
      },
      body: JSON.stringify({ name: 'test' }),
    });
    expect(data).toEqual({ done: true });
  });
});
