#!/usr/bin/env python3
from app import create_app, db
from app.models import Yazar, Yayinevi, Kategori, Kitap, Musteri, Personel, Satis, SatisDetay
import inspect
import os

def model_to_dot(model_classes):
    dot = [
        'digraph G {', 
        '  rankdir=LR;', 
        '  node [shape=record, fontname="Arial", fontsize=12];', 
        '  edge [fontname="Arial", fontsize=10];',
        '  // Set graph attributes',
        '  graph [bgcolor="#F5F5F5", splines=polyline];',
        '  // Define node styles for different types of entities',
        '  node [style=filled, fillcolor="#E3F2FD"];',
    ]
    
    # Add nodes for each model
    for model_class in model_classes:
        table_name = getattr(model_class, '__tablename__', model_class.__name__)
        attributes = []
        
        # Color tables by category
        fillcolor = "#E3F2FD"  # Default blue-ish
        if table_name in ["Yazarlar", "Yayinevleri", "Kategoriler"]:
            fillcolor = "#E8F5E9"  # Green-ish for reference tables
        elif table_name in ["Kitaplar"]:
            fillcolor = "#FFECB3"  # Yellow-ish for main content tables
        elif table_name in ["Satislar", "SatisDetaylari"]:
            fillcolor = "#FFCDD2"  # Red-ish for transaction tables
        elif table_name in ["Musteriler", "Personeller"]:
            fillcolor = "#E1BEE7"  # Purple-ish for person tables
        
        for attr_name, attr in inspect.getmembers(model_class):
            if not attr_name.startswith('_') and not callable(attr) and not attr_name == 'metadata':
                if hasattr(attr, 'type') and hasattr(attr, 'primary_key'):
                    # This is a Column
                    attrs = []
                    if attr.primary_key:
                        attrs.append('PK')
                    if attr.foreign_keys:
                        attrs.append('FK')
                    if attr.unique:
                        attrs.append('UQ')
                    if not attr.nullable:
                        attrs.append('NOT NULL')
                    
                    attr_type = str(attr.type).replace('DECIMAL', 'NUMERIC')
                    
                    if attrs:
                        attrs_str = ' [' + ', '.join(attrs) + ']'
                    else:
                        attrs_str = ''
                    
                    attributes.append(f"{attr_name} : {attr_type}{attrs_str}")
        
        # Format the node label with table name and attributes
        label = f"{table_name}|{{'\\n'.join(attributes)}}"
        dot.append(f'  "{table_name}" [label="{label}", fillcolor="{fillcolor}"];')
    
    # Add edges for relationships
    for model_class in model_classes:
        table_name = getattr(model_class, '__tablename__', model_class.__name__)
        
        for attr_name, attr in inspect.getmembers(model_class):
            if not attr_name.startswith('_') and not callable(attr) and not attr_name == 'metadata':
                if hasattr(attr, 'foreign_keys') and attr.foreign_keys:
                    for fk in attr.foreign_keys:
                        target_table = fk.target_fullname.split('.')[0]
                        dot.append(f'  "{table_name}" -> "{target_table}" [label="  {attr_name}  ", color="#2196F3", penwidth=1.5];')
    
    # Add special handling for many-to-many relationships
    # In this case, we add the KitapYazarlari relationship
    dot.append('  "KitapYazarlari" [label="KitapYazarlari|{KitapID : INTEGER [PK, FK]\\nYazarID : INTEGER [PK, FK]}", fillcolor="#FFF9C4"];')
    dot.append('  "KitapYazarlari" -> "Kitaplar" [label="  KitapID  ", color="#4CAF50", penwidth=1.5, style="dashed"];')
    dot.append('  "KitapYazarlari" -> "Yazarlar" [label="  YazarID  ", color="#4CAF50", penwidth=1.5, style="dashed"];')
    
    dot.append('}')
    return '\n'.join(dot)

def generate_diagram():
    print("Generating database diagram...")
    model_classes = [Yazar, Yayinevi, Kategori, Kitap, Musteri, Personel, Satis, SatisDetay]
    
    # Generate DOT format
    dot_content = model_to_dot(model_classes)
    
    # Write DOT file
    with open('database_schema.dot', 'w') as f:
        f.write(dot_content)
    
    print("DOT file created as 'database_schema.dot'")
    
    # Try to generate PNG if Graphviz is installed
    try:
        # Create both PNG and SVG for better quality
        os.system('dot -Tpng database_schema.dot -o database_schema.png')
        print("PNG diagram created as 'database_schema.png'")
        
        os.system('dot -Tsvg database_schema.dot -o database_schema.svg')
        print("SVG diagram created as 'database_schema.svg' (vector format for better zooming)")
    except Exception as e:
        print(f"Error generating diagrams: {e}")
        print("You can manually convert the DOT file to an image using the Graphviz 'dot' command:")
        print("  dot -Tpng database_schema.dot -o database_schema.png")
        print("  dot -Tsvg database_schema.dot -o database_schema.svg")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        generate_diagram() 