{{/* Chart Name + Chart Version */}}
{{- define "spring-music.name" -}}
{{ .Chart.Name }}-{{ .Chart.Version | replace "." "-" }}
{{- end }}

{{/* */}}
{{- define "spring.labels" -}}
generator: helm
app-name: {{ .Chart.Name }}
date: {{ now | htmlDate }}
version: {{ .Chart.Version }}
{{- end }}
