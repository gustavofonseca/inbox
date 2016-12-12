import django.dispatch


# Evento disparado após a transação ``transactions.deposit_package`` ter
# sido efetivada com sucesso.
# O argumento ``instance`` deve ser a instância de ``models.Deposit``
# recém criada.
package_deposited = django.dispatch.Signal(providing_args=["instance"])


# Evento disparado após a criação de todas as instâncias de
# ``models.PackageMember`` pela task ``tasks.create_package_members``.
# O argumento ``instance`` deve ser a instância de ``models.Package`` que
# contém os membros.
package_members_created = django.dispatch.Signal(providing_args=["instance"])

