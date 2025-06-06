import { NextResponse } from "next/server";

/**
 * Middleware para redirecionar usuários não autenticados.
 * @param {NextRequest} request Objeto da requisição Next.js
 */
export function middleware(request) {
  const isDev = process.env.NODE_ENV === "development";
  if (isDev) {
    console.log("Cookies disponíveis:", request.cookies.getAll());
  }

  const token = request.cookies.get("access_token")?.value;

  if (!token) {
    const url = request.nextUrl.clone();
    url.pathname = "/";
    if (isDev) {
      console.log("Redirecionando para / devido à falta de token.");
    }
    return NextResponse.redirect(url);
  }

  if (isDev) {
    console.log("Token encontrado, continuando:", token);
  }
  return NextResponse.next();
}

// Configura as rotas onde o middleware será aplicado
export const config = {
  matcher: ["/protected-route/:path*", "/dashboard/:path*"], // Defina suas rotas protegidas aqui
};
