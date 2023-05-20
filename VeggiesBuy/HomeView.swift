//
//  HomeView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI

struct Vegetable: Hashable, Codable {
    let sname: String
    let vname: String
    let price: Float
    let unit: String?
}

// fetch store names
class ViewModel: ObservableObject {
    @Published var vegetables: [Vegetable] = []
    @Published var searchQuery: String = ""
    
    var filteredVegetables: [Vegetable] {
        if searchQuery.isEmpty {
            return vegetables
        } else {
            return vegetables.filter { vegetable in
                vegetable.vname.localizedCaseInsensitiveContains(searchQuery)
            }
        }
    }
    
    func fetch() {
        guard let url = URL(string: "http://localhost:5006/item") else {
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, _,
            error in
            guard let data = data, error == nil else {
                return
            }
            
            // convert to JSON
            do {
                let vegetables = try JSONDecoder().decode([Vegetable].self, from: data)
                
                DispatchQueue.main.async {
                    self?.vegetables = vegetables
                }
            }
            catch {
                print(error)
            }
        }
        task.resume()
    }
}

struct HomeView: View {
    @StateObject var viewModel = ViewModel()
    
    var body: some View {
        NavigationView {
            VStack {
                
                List {
                    ForEach(viewModel.filteredVegetables, id: \.self) { vegetable in
                        VStack {
                            HStack {
                                Text(vegetable.vname.capitalized)
                                    .bold()
                                    .font(.system(size: 18))
                                Spacer()
                                if let unit = vegetable.unit {
                                    Text("$\(vegetable.price, specifier: "%.2f")/\(unit)")
                                } else {
                                    Text("$\(vegetable.price, specifier: "%.2f")")
                                }
                            }
                            Text(vegetable.sname)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .padding(.vertical, 1)
                        }
                        
                    }
                }
            }
            .searchable(text: $viewModel.searchQuery, prompt: "Search vegetables")
            .navigationBarTitle("Home")
            .onAppear {
                viewModel.fetch()
            }
        }
    }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
    }
}
