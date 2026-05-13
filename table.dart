import 'dart:io';

void main() {
  stdout.write('Entrez un nombre: ');
  String? input = stdin.readLineSync();
  if (input == null || input.trim().isEmpty) {
    print('Aucune entrée fournie.');
    return;
  }
  final value = input.trim();
  final n = int.tryParse(value);
  if (n == null) {
    print('Entrée invalide. Veuillez entrer un entier.');
    return;
  }
  print('Table de multiplication de $n:');
  for (var i = 1; i <= 10; i++) {
    print('$n x $i = ${n * i}');
  }
}
