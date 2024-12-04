import { NextResponse } from "next/server";

/**
 * Middleware para redirecionar usuários não autenticados.
 * @param {NextRequest} request Objeto da requisição Next.js
 */
export function middleware(request) {
  console.log("Cookies disponíveis:", request.cookies.getAll());

  const token = request.cookies.get("access_token")?.value;

  if (!token) {
    const url = request.nextUrl.clone();
    url.pathname = "/";
    console.log("Redirecionando para / devido à falta de token.");
    return NextResponse.redirect(url);
  }

  console.log("Token encontrado, continuando:", token);
  return NextResponse.next();
}

// Configura as rotas onde o middleware será aplicado
export const config = {
  matcher: ["/protected-route/:path*", "/dashboard/:path*"], // Defina suas rotas protegidas aqui
};
