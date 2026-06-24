export interface Libro {
    id: number;
    nt: string;
    etiqueta: string; 
    titulo: string;
    autor: string;
    ejemplares: number;
    foto?: File | string; // Puede ser un File o una URL de string
    estado: string;
    estado_display?: string; // Campo opcional para mostrar el estado de manera más amigable
    registrado_en?: string; // Campo opcional para mostrar la fecha de registro en formato legible
    actualizado_en?: string; // Campo opcional para mostrar la fecha de última actualización en formato legible
}

export interface Prestamo {
    id?: number;
    libro: number;
    libro_titulo?: string;
    libro_autor?: string;
    libro_etiqueta?: string;
    libro_nt?: string;
    nombre_lector: string;
    fecha_prestamo?: string;
    fecha_devolucion: string;
    estado: 'vigente' | 'vencido' | 'devuelto';
    estado_display?: string;
    esta_vencido?: boolean;
    dias_restantes?: number;
    creado_en?: string;
}

export interface ApiResponse<T> {
    success: boolean;
    data: T;
    message?: string;
    status: number;
}