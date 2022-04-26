FROM mcr.microsoft.com/dotnet/aspnet:5.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY ["dotnet-core/dotnet-core.csproj", "dotnet-core/"]
RUN dotnet restore "dotnet-core/dotnet-core.csproj"
COPY . .
WORKDIR "/src/dotnet-core"
RUN dotnet build "dotnet-core.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "dotnet-core.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "dotnet-core.dll"]
